from __future__ import annotations

import logging

import discord
from discord.ext import commands

from bot.companion import Companion
from bot.config import load_settings
from bot.memory import MemoryStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger("discord-companion")

settings = load_settings()
memory = MemoryStore(settings.memory_file)
companion = Companion(
    api_key=settings.openai_api_key,
    model=settings.openai_model,
    memory=memory,
    min_confidence=settings.participation_min_confidence,
    cooldown_seconds=settings.participation_cooldown_seconds,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def allowed(message: discord.Message) -> bool:
    if message.author.bot:
        return False
    if settings.allowed_user_ids and message.author.id not in settings.allowed_user_ids:
        return False
    if settings.allowed_channel_id is not None and message.channel.id != settings.allowed_channel_id:
        return False
    return True


@bot.event
async def on_ready() -> None:
    log.info("Companion online como %s", bot.user)


@bot.event
async def on_message(message: discord.Message) -> None:
    if not allowed(message):
        return

    await bot.process_commands(message)

    channel = message.channel
    if not hasattr(channel, "history"):
        return

    recent: list[dict[str, str]] = []
    async for item in channel.history(limit=settings.max_context_messages, oldest_first=False):
        if item.author.bot and item.author.id != bot.user.id:
            continue
        recent.append({"name": item.author.display_name, "content": item.content})

    recent.reverse()
    if not recent:
        return

    try:
        decision = companion.decide(recent)
        log.info("Decisão: speak=%s confidence=%.2f reason=%s", decision.speak, decision.confidence, decision.reason)
        if not decision.speak or decision.confidence < settings.participation_min_confidence:
            return

        reply = companion.respond(recent)
        if reply:
            await channel.send(reply)
    except Exception:
        log.exception("Erro ao processar a conversa")


@bot.command(name="entrar")
@commands.has_permissions(administrator=True)
async def entrar(ctx: commands.Context) -> None:
    await ctx.send("Estou aqui. Vou acompanhar a conversa sem tentar falar a cada cinco segundos.")


@bot.command(name="status")
async def status(ctx: commands.Context) -> None:
    await ctx.send("Companion online. Núcleo de conversa ativo; voz será adicionada na próxima camada.")


if __name__ == "__main__":
    bot.run(settings.discord_token)
