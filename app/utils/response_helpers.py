"""Helper functions for API responses"""

import uuid
from typing import Optional, TypeVar
from fastapi import Request
from app.schemas.base import StandardResponse

T = TypeVar("T")


def create_response(
    message: str,
    status_code: int,
    data: Optional[T] = None,
    request_id: Optional[str] = None
) -> StandardResponse[T]:
    """
    Create a standardized response (works for both success and error)

    Args:
        message: Response message
        status_code: HTTP status code
        data: Response data (None for errors)
        request_id: Optional request ID (used for logging, not included in response)

    Returns:
        StandardResponse instance
    """
    # Note: request_id is used for logging but not included in response body
    return StandardResponse(
        message=message,
        status_code=status_code,
        data=data
    )


def get_request_id(request: Request) -> str:
    """
    Get or generate request ID from request headers

    Args:
        request: FastAPI request object

    Returns:
        Request ID string
    """
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())
    return request_id
