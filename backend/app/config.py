import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "Digital Fossil"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "digital-fossil-dev-secret-key-32bytes-secure!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'digital_fossil.db'}")

    # Thresholds
    DEFAULT_SESSION_THRESHOLD_SECONDS: int = int(os.getenv("DEFAULT_SESSION_THRESHOLD_SECONDS", "120"))
    DEFAULT_MIN_RELATIONSHIP_SCORE: float = float(os.getenv("DEFAULT_MIN_RELATIONSHIP_SCORE", "0.35"))
    DEFAULT_ANOMALY_CONTAMINATION: float = float(os.getenv("DEFAULT_ANOMALY_CONTAMINATION", "0.10"))

    # Optional LLM
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "none")

    # Safe Collector Monitored Directory
    TEST_MONITOR_DIR: Path = BASE_DIR / "data" / "test_folder"
    REPORTS_DIR: Path = BASE_DIR / "reports" / "generated"

    class Config:
        arbitrary_types_allowed = True

settings = Settings()

# Ensure necessary data directories exist
settings.TEST_MONITOR_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
