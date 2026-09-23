"""
Centralized application configuration.

All values are loaded from environment variables (see .env.example).
Evaluation weights live here as the single source of truth so they are
never hardcoded inside evaluation modules (Rule #15 in project spec).
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Database ---
    DATABASE_URL: str = "postgresql://interview_user:interview_pass@localhost:5432/interview_db"

    # --- Auth ---
    JWT_SECRET_KEY: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- NLP / ML ---
    SBERT_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # --- Evaluation weights ---
    EVAL_WEIGHT_RELEVANCE: float = 0.25
    EVAL_WEIGHT_SEMANTIC: float = 0.30
    EVAL_WEIGHT_CONCEPT: float = 0.20
    EVAL_WEIGHT_COMPLETENESS: float = 0.15
    EVAL_WEIGHT_GRAMMAR: float = 0.10

    # --- Adaptive difficulty ---
    ADAPTIVE_SCORE_INCREASE: int = 80
    ADAPTIVE_SCORE_MAINTAIN_LOW: int = 50

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # --- App ---
    ENVIRONMENT: str = "development"
    DEFAULT_QUESTIONS_PER_INTERVIEW: int = 10

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def evaluation_weights(self) -> dict:
        return {
            "relevance": self.EVAL_WEIGHT_RELEVANCE,
            "semantic": self.EVAL_WEIGHT_SEMANTIC,
            "concept": self.EVAL_WEIGHT_CONCEPT,
            "completeness": self.EVAL_WEIGHT_COMPLETENESS,
            "grammar": self.EVAL_WEIGHT_GRAMMAR,
        }

    def validate_weights(self) -> None:
        total = sum(self.evaluation_weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Evaluation weights must sum to 1.0, got {total}. "
                f"Check EVAL_WEIGHT_* environment variables."
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_weights()
    return settings
