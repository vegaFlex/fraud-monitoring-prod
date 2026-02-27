from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pathlib import Path

# load .env automatically
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


def _get_env(name: str, default: str | None = None) -> str:
    val = os.getenv(name, default)
    if val is None or val == "":
        raise RuntimeError(f"Missing required env var: {name}")
    return val


@dataclass(frozen=True)
class Settings:
    app_env: str
    openml_dataset_id: int

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_name: str
    model_stage: str


def load_settings() -> Settings:
    return Settings(
        app_env=_get_env("APP_ENV", "dev"),
        openml_dataset_id=int(_get_env("OPENML_DATASET_ID", "42175")),
        postgres_host=_get_env("POSTGRES_HOST"),
        postgres_port=int(_get_env("POSTGRES_PORT")),
        postgres_db=_get_env("POSTGRES_DB"),
        postgres_user=_get_env("POSTGRES_USER"),
        postgres_password=_get_env("POSTGRES_PASSWORD"),
        model_name=_get_env("MODEL_NAME", "fraud_model"),
        model_stage=_get_env("MODEL_STAGE", "production"),
    )