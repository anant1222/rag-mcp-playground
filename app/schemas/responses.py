"""Data models for API responses (these go inside the 'data' field)"""

from pydantic import BaseModel, Field


class AskResponseData(BaseModel):
    """Data model for /ask endpoint response (goes inside 'data' field)"""
    response: str = Field(..., description="LLM generated response")
    model: str = Field(..., description="Model used for generation")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "The capital of France is Paris.",
                "model": "gpt-3.5-turbo"
            }
        }


class ChatResponseData(BaseModel):
    """Data model for /chat endpoint response (goes inside 'data' field)"""
    response: str = Field(..., description="LLM generated response")
    model: str = Field(..., description="Model used for generation")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Machine learning is a subset of artificial intelligence...",
                "model": "gpt-3.5-turbo"
            }
        }


class StreamResponseData(BaseModel):
    """Data model metadata for /stream endpoint (goes inside 'data' field)"""
    model: str = Field(..., description="Model used for streaming")
    message: str = Field(..., description="Streaming status message")

    class Config:
        json_schema_extra = {
            "example": {
                "model": "gpt-3.5-turbo",
                "message": "Streaming started"
            }
        }
