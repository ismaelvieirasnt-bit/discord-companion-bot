from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _int_list(value: str | None) -> set[int]:
    if not value:
        return set()
    return {int(item.strip()) for item in value.split(",") if item.strip()}


@dataclass(frozen=True)
class Settings:
    discord_token: str
    openai_api_key: str
    openai_model: str
    allowed_user_ids: set[int]
    allowed_channel_id: int | None
    memory_file: Path
    participation_min_confidence: float
    participation_cooldown_seconds: float
    max_context_messages: int



def load_settings() -> Settings:
    discord_token = os.getenv("DISCORD_TOKEN", "").strip()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not discord_token:
        raise RuntimeError("DISCORD_TOKEN is not configured. Copy .env.example to .env and fill it in.")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Copy .env.example to .env and fill it in.")

    raw_channel = os.getenv("ALLOWED_CHANNEL_ID", "").strip()
    return Settings(
        discord_token=discord_token,
        openai_api_key=openai_api_key,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.6").strip(),
        allowed_user_ids=_int_list(os.getenv("ALLOWED_USER_IDS")),
        allowed_channel_id=int(raw_channel) if raw_channel else None,
        memory_file=Path(os.getenv("MEMORY_FILE", "data/memory.json")),
        participation_min_confidence=float(os.getenv("PARTICIPATION_MIN_CONFIDENCE", "0.68")),
        participation_cooldown_seconds=float(os.getenv("PARTICIPATION_COOLDOWN_SECONDS", "25")),
        max_context_messages=int(os.getenv("MAX_CONTEXT_MESSAGES", "18")),
    )
