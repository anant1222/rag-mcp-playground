"""Error handling middleware"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import (
    LLMServiceError,
    LLMValidationError,
    LLMTimeoutError,
    LLMAPIError
)
from app.utils.response_helpers import create_response, get_request_id
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors"""
    request_id = get_request_id(request)
    error_response = create_response(
        message="Validation error",
        status_code=status.HTTP_400_BAD_REQUEST,
        data=None,
        request_id=request_id
    )
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.model_dump()
    )


async def llm_validation_exception_handler(
    request: Request,
    exc: LLMValidationError
) -> JSONResponse:
    """Handle LLM validation errors"""
    request_id = get_request_id(request)
    error_response = create_response(
        message=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST,
        data=None,
        request_id=request_id
    )
    logger.warning(f"LLM validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.model_dump()
    )


async def llm_timeout_exception_handler(
    request: Request,
    exc: LLMTimeoutError
) -> JSONResponse:
    """Handle LLM timeout errors"""
    request_id = get_request_id(request)
    error_response = create_response(
        message=str(exc),
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        data=None,
        request_id=request_id
    )
    logger.error(f"LLM timeout error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content=error_response.model_dump()
    )


async def llm_api_exception_handler(
    request: Request,
    exc: LLMAPIError
) -> JSONResponse:
    """Handle LLM API errors"""
    request_id = get_request_id(request)
    error_response = create_response(
        message=str(exc),
        status_code=status.HTTP_502_BAD_GATEWAY,
        data=None,
        request_id=request_id
    )
    logger.error(f"LLM API error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content=error_response.model_dump()
    )


async def llm_service_exception_handler(
    request: Request,
    exc: LLMServiceError
) -> JSONResponse:
    """Handle general LLM service errors"""
    request_id = get_request_id(request)
    error_response = create_response(
        message=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=None,
        request_id=request_id
    )
    logger.error(f"LLM service error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle general exceptions"""
    request_id = get_request_id(request)
    error_response = create_response(
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        data=None,
        request_id=request_id
    )
    logger.exception(f"Unexpected error: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


def setup_error_handlers(app):
    """Setup all error handlers for the FastAPI app"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(LLMValidationError, llm_validation_exception_handler)
    app.add_exception_handler(LLMTimeoutError, llm_timeout_exception_handler)
    app.add_exception_handler(LLMAPIError, llm_api_exception_handler)
    app.add_exception_handler(LLMServiceError, llm_service_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
