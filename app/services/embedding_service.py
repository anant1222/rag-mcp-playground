"""Embedding service for generating vector embeddings"""

from typing import List
import numpy as np
from openai import AsyncOpenAI, APIError
from app.config import settings
from app.utils.logger import get_logger
from app.utils.exceptions import LLMAPIError

logger = get_logger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize embedding service

        Args:
            model: OpenAI embedding model name
        """
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats

        Raises:
            LLMAPIError: If embedding generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text.strip()
            )

            if not response.data or len(response.data) == 0:
                raise ValueError("Empty embedding response")

            return response.data[0].embedding

        except APIError as e:
            logger.error(f"OpenAI API error generating embedding: {str(e)}")
            raise LLMAPIError(f"Failed to generate embedding: {str(e)}", original_error=e)
        except Exception as e:
            logger.error(f"Unexpected error generating embedding: {str(e)}")
            raise LLMAPIError(f"Unexpected error: {str(e)}", original_error=e)

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing)

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            LLMAPIError: If embedding generation fails
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        try:
            # Filter empty texts
            valid_texts = [text.strip() for text in texts if text and text.strip()]

            if not valid_texts:
                raise ValueError("No valid texts to embed")

            response = await self.client.embeddings.create(
                model=self.model,
                input=valid_texts
            )

            if len(response.data) != len(valid_texts):
                raise ValueError(f"Expected {len(valid_texts)} embeddings, got {len(response.data)}")

            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings

        except APIError as e:
            logger.error(f"OpenAI API error generating batch embeddings: {str(e)}")
            raise LLMAPIError(f"Failed to generate batch embeddings: {str(e)}", original_error=e)
        except Exception as e:
            logger.error(f"Unexpected error generating batch embeddings: {str(e)}")
            raise LLMAPIError(f"Unexpected error: {str(e)}", original_error=e)
