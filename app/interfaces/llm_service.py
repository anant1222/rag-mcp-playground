"""Interface for LLM service implementations"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class ILLMService(ABC):
    """Abstract interface for LLM service implementations"""

    @abstractmethod
    async def ask(self, prompt: str, timeout: Optional[int] = None) -> str:
        """
        Simple LLM response to a user prompt

        Args:
            prompt: User's question or prompt
            timeout: Optional timeout override

        Returns:
            LLM response text

        Raises:
            ValueError: If prompt is invalid
            TimeoutError: If request times out
            RuntimeError: If API call fails
        """
        pass

    @abstractmethod
    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        timeout: Optional[int] = None
    ) -> str:
        """
        Chat with system and user prompts

        Args:
            system_prompt: System instruction/context
            user_prompt: User's message
            timeout: Optional timeout override

        Returns:
            LLM response text

        Raises:
            ValueError: If prompts are invalid
            TimeoutError: If request times out
            RuntimeError: If API call fails
        """
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> AsyncIterator[str]:
        """
        Stream LLM response

        Args:
            prompt: User's prompt
            system_prompt: Optional system instruction
            timeout: Optional timeout override

        Yields:
            Chunks of LLM response text

        Raises:
            ValueError: If prompt is invalid
            TimeoutError: If request times out
            RuntimeError: If API call fails
        """
        pass
