"""
LLM client for NVIDIA NIM integration.

Provides a generic interface for LLM interactions, isolating NVIDIA-specific implementation.
"""

from typing import Optional

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from src.config import get_config, validate_llm_config


class LLMClient:
    """
    Generic LLM client interface.

    Wraps NVIDIA NIM client and provides a simple interface for the application.
    """

    def __init__(self, require_api_key: bool = False):
        """
        Initialize LLM client.

        Args:
            require_api_key: If True, validates that API key is configured.
                            Set to False for tests that use mocks.

        Raises:
            ValueError: If API key is required but not configured.
        """
        self.config = get_config()

        if require_api_key:
            validate_llm_config(self.config)

        self._client: Optional[ChatNVIDIA] = None

    @property
    def client(self) -> ChatNVIDIA:
        """
        Get or create the NVIDIA NIM client.

        Returns:
            ChatNVIDIA instance.

        Raises:
            ValueError: If API key is not configured.
        """
        if self._client is None:
            if not self.config.nvidia_api_key or self.config.nvidia_api_key == "your_nvidia_api_key_here":
                raise ValueError(
                    "NVIDIA_API_KEY is not configured. "
                    "Please set it in your .env file or environment variables."
                )

            self._client = ChatNVIDIA(
                model=self.config.nvidia_model,
                api_key=self.config.nvidia_api_key,
                base_url=self.config.nvidia_base_url,
            )

        return self._client

    def invoke(
        self,
        messages: list[BaseMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Invoke the LLM with a list of messages.

        Args:
            messages: List of messages (SystemMessage, HumanMessage, etc.).
            temperature: Sampling temperature (0.0 to 1.0).
            max_tokens: Maximum tokens to generate.

        Returns:
            LLM response as string.

        Raises:
            ValueError: If API key is not configured.
        """
        response = self.client.invoke(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.content

    def invoke_with_system_prompt(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Invoke the LLM with a system prompt and user message.

        Args:
            system_prompt: System prompt for the LLM.
            user_message: User message to process.
            temperature: Sampling temperature (0.0 to 1.0).
            max_tokens: Maximum tokens to generate.

        Returns:
            LLM response as string.

        Raises:
            ValueError: If API key is not configured.
        """
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
        return self.invoke(messages, temperature=temperature, max_tokens=max_tokens)

    def is_configured(self) -> bool:
        """
        Check if the LLM client is properly configured.

        Returns:
            True if API key is configured, False otherwise.
        """
        return bool(
            self.config.nvidia_api_key
            and self.config.nvidia_api_key != "your_nvidia_api_key_here"
        )


# Global LLM client instance
_llm_client: Optional[LLMClient] = None


def get_llm(require_api_key: bool = False) -> LLMClient:
    """
    Get the global LLM client instance.

    Args:
        require_api_key: If True, validates that API key is configured.

    Returns:
        LLMClient instance.
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient(require_api_key=require_api_key)
    return _llm_client
