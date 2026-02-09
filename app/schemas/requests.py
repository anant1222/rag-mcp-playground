"""Request schemas for API endpoints"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.config import settings


class AskRequest(BaseModel):
    """Request schema for /ask endpoint"""
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_MESSAGE_LENGTH,
        description="User's question or prompt"
    )
    timeout: Optional[int] = Field(
        None,
        ge=1,
        le=300,
        description="Request timeout in seconds (1-300)"
    )

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "What is the capital of France?",
                "timeout": 30
            }
        }


class ChatRequest(BaseModel):
    """Request schema for /chat endpoint"""
    system_prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_SYSTEM_MESSAGE_LENGTH,
        description="System instruction or context"
    )
    user_prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_MESSAGE_LENGTH,
        description="User's message"
    )
    timeout: Optional[int] = Field(
        None,
        ge=1,
        le=300,
        description="Request timeout in seconds (1-300)"
    )

    @field_validator('system_prompt', 'user_prompt')
    @classmethod
    def validate_prompts(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "system_prompt": "You are a helpful assistant.",
                "user_prompt": "What is machine learning?",
                "timeout": 30
            }
        }


class StreamRequest(BaseModel):
    """Request schema for /stream endpoint"""
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_MESSAGE_LENGTH,
        description="User's prompt"
    )
    system_prompt: Optional[str] = Field(
        None,
        max_length=settings.MAX_SYSTEM_MESSAGE_LENGTH,
        description="Optional system instruction"
    )
    timeout: Optional[int] = Field(
        None,
        ge=1,
        le=600,
        description="Stream timeout in seconds (1-600)"
    )

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()

    @field_validator('system_prompt')
    @classmethod
    def validate_system_prompt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            return None
        return v.strip() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Tell me a short story",
                "system_prompt": "You are a creative writer.",
                "timeout": 60
            }
        }
