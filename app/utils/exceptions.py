"""Custom exceptions for the application"""


class LLMServiceError(Exception):
    """Base exception for LLM service errors"""
    pass


class LLMValidationError(LLMServiceError):
    """Exception raised for validation errors"""
    pass


class LLMTimeoutError(LLMServiceError):
    """Exception raised for timeout errors"""
    pass


class LLMAPIError(LLMServiceError):
    """Exception raised for API errors"""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error
