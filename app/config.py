import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Timeout Configuration (in seconds)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    STREAM_TIMEOUT: int = int(os.getenv("STREAM_TIMEOUT", "60"))

    # API Configuration
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "10000"))
    MAX_SYSTEM_MESSAGE_LENGTH: int = int(os.getenv("MAX_SYSTEM_MESSAGE_LENGTH", "5000"))

settings = Settings()
