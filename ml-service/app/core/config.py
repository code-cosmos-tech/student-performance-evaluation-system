from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv(".env.example")


class Settings(BaseModel):
    # App
    app_name: str = os.getenv("APP_NAME")
    app_version: str = os.getenv("APP_VERSION")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # API
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    api_service: str = os.getenv("API_SERVICE", "ml")

    # CORS
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "").split(",")

    # Model paths
    model_path: str = os.getenv("MODEL_PATH")
    scaler_path: str = os.getenv("SCALER_PATH")
    encoders_path: str = os.getenv("ENCODERS_PATH")


settings = Settings()
