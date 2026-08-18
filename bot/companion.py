from __future__ import annotations

import json
import time
from dataclasses import dataclass

from openai import OpenAI

from bot.memory import MemoryStore
from bot.personality import SYSTEM_PROMPT


@dataclass
class Decision:
    speak: bool
    confidence: float
    reason: str


class Companion:
    def __init__(self, api_key: str, model: str, memory: MemoryStore, min_confidence: float, cooldown_seconds: float) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.memory = memory
        self.min_confidence = min_confidence
        self.cooldown_seconds = cooldown_seconds
        self.last_spoke_at = 0.0

    def _recent_context(self, messages: list[dict[str, str]]) -> str:
        return "\n".join(f"{m['name']}: {m['content']}" for m in messages)

    def decide(self, messages: list[dict[str, str]]) -> Decision:
        if time.monotonic() - self.last_spoke_at < self.cooldown_seconds:
            return Decision(False, 0.0, "cooldown")

        prompt = f"""
Analisa a conversa abaixo e decide se o Companion deve participar agora.

Só responde com JSON válido neste formato:
{{"speak": true|false, "confidence": 0.0, "reason": "..."}}

Participar é apropriado quando houver algo genuinamente relevante: uma pergunta que aprofunde, uma contradição, uma perspectiva nova, uma conexão criativa ou uma resposta diretamente implícita.
Não participar é apropriado quando a conversa estiver fluindo bem sem necessidade de intervenção, quando a contribuição seria apenas repetição ou quando seria intrusivo.

CONVERSA:
{self._recent_context(messages)}
""".strip()

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        raw = response.output_text.strip()
        try:
            data = json.loads(raw)
            return Decision(
                speak=bool(data.get("speak", False)),
                confidence=float(data.get("confidence", 0.0)),
                reason=str(data.get("reason", "")),
            )
        except (json.JSONDecodeError, TypeError, ValueError):
            return Decision(False, 0.0, "decision_parse_error")

    def respond(self, messages: list[dict[str, str]]) -> str:
        context = self._recent_context(messages)
        prompt = f"""
Aqui está a memória persistente:
{self.memory.as_text()}

Aqui está a conversa atual:
{context}

Entre na conversa como Companion. Responde apenas com a fala que deve aparecer no Discord.
Não descrevas o que estás fazendo. Não uses prefácios como 'como IA'.
Sê natural, específico e relativamente breve. Faz uma pergunta quando ela realmente abrir uma camada nova.
""".strip()

        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        self.last_spoke_at = time.monotonic()
        return response.output_text.strip()
