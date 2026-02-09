"""LLM service implementation"""

import asyncio
from typing import AsyncIterator, Optional
from openai import AsyncOpenAI, APIError
from app.config import settings
from app.interfaces.llm_service import ILLMService
from app.utils.exceptions import LLMValidationError, LLMTimeoutError, LLMAPIError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAILLMService(ILLMService):
    """OpenAI implementation of LLM service"""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_MODEL
        self.timeout = settings.REQUEST_TIMEOUT

    @property
    def model(self) -> str:
        """Get the model name"""
        return self._model

    async def ask(self, prompt: str, timeout: Optional[int] = None) -> str:
        """Simple LLM response to a user prompt"""
        if not prompt or not prompt.strip():
            raise LLMValidationError("Prompt cannot be empty")

        timeout = timeout or self.timeout

        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                    max_tokens=1000
                ),
                timeout=timeout
            )

            if not response.choices or not response.choices[0].message.content:
                raise LLMValidationError("Empty response from LLM")

            return response.choices[0].message.content.strip()

        except asyncio.TimeoutError:
            logger.error(f"Request timed out after {timeout} seconds")
            raise LLMTimeoutError(f"Request timed out after {timeout} seconds")
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise LLMAPIError(f"LLM API error: {str(e)}", original_error=e)
        except Exception as e:
            logger.error(f"Unexpected error in ask: {str(e)}")
            raise LLMAPIError(f"Unexpected error: {str(e)}", original_error=e)

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout: Optional[int] = None
    ) -> str:
        """Chat with system and user prompts"""
        if not system_prompt or not system_prompt.strip():
            raise LLMValidationError("System prompt cannot be empty")
        if not user_prompt or not user_prompt.strip():
            raise LLMValidationError("User prompt cannot be empty")

        timeout = timeout or self.timeout

        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                ),
                timeout=timeout
            )

            if not response.choices or not response.choices[0].message.content:
                raise LLMValidationError("Empty response from LLM")

            return response.choices[0].message.content.strip()

        except asyncio.TimeoutError:
            logger.error(f"Request timed out after {timeout} seconds")
            raise LLMTimeoutError(f"Request timed out after {timeout} seconds")
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise LLMAPIError(f"LLM API error: {str(e)}", original_error=e)
        except Exception as e:
            logger.error(f"Unexpected error in chat: {str(e)}")
            raise LLMAPIError(f"Unexpected error: {str(e)}", original_error=e)

    async def stream( self, prompt: str, system_prompt: Optional[str] = None, timeout: Optional[int] = None
    ) -> AsyncIterator[str]:
        """Stream LLM response"""
        if not prompt or not prompt.strip():
            raise LLMValidationError("Prompt cannot be empty")

        timeout = timeout or settings.STREAM_TIMEOUT

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000,
                    stream=True
                ),
                timeout=timeout
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except asyncio.TimeoutError:
            logger.error(f"Stream timed out after {timeout} seconds")
            raise LLMTimeoutError(f"Stream timed out after {timeout} seconds")
        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise LLMAPIError(f"LLM API error: {str(e)}", original_error=e)
        except Exception as e:
            logger.error(f"Unexpected error in stream: {str(e)}")
            raise LLMAPIError(f"Unexpected error: {str(e)}", original_error=e)


# Singleton instance
_llm_service: Optional[ILLMService] = None


def get_llm_service() -> ILLMService:
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = OpenAILLMService()
    return _llm_service
