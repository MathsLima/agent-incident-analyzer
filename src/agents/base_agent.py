"""
Base agent class for all specialized agents.
"""

from pathlib import Path
from typing import Any

from src.llm import get_llm


class BaseAgent:
    """
    Base class for all specialized agents.

    Provides common functionality for loading prompts and invoking the LLM.
    """

    def __init__(self, prompt_file: str, require_api_key: bool = True):
        """
        Initialize the agent.

        Args:
            prompt_file: Name of the prompt file in the prompts/ directory.
            require_api_key: If True, validates that API key is configured.
        """
        self.prompt_file = prompt_file
        self.llm = get_llm(require_api_key=require_api_key)
        self._system_prompt: str = ""

    @property
    def system_prompt(self) -> str:
        """
        Get the system prompt for this agent.

        Returns:
            System prompt as string.
        """
        if not self._system_prompt:
            prompt_path = Path(__file__).parent.parent.parent / "prompts" / self.prompt_file
            with open(prompt_path, "r") as f:
                self._system_prompt = f.read()
        return self._system_prompt

    def invoke(self, user_message: str, **kwargs: Any) -> str:
        """
        Invoke the agent with a user message.

        Args:
            user_message: User message to process.
            **kwargs: Additional arguments for LLM invocation.

        Returns:
            Agent response as string.
        """
        return self.llm.invoke_with_system_prompt(
            system_prompt=self.system_prompt,
            user_message=user_message,
            **kwargs,
        )
