"""Base response schemas for unified API response format"""

from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    """
    Unified standard response format for ALL API endpoints (success and error)

    All API responses follow this structure:
    {
        "message": str,
        "status_code": int,
        "data": T | null
    }
    """
    message: str = Field(..., description="Human-readable message")
    status_code: int = Field(..., description="HTTP status code")
    data: Optional[T] = Field(None, description="Response data payload (null for errors)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Request processed successfully",
                "status_code": 200,
                "data": {}
            }
        }
