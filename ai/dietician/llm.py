from abc import ABC, abstractmethod

import requests

from ai.dietician.context import DietConversationContext
from ai.dietician.conversation import DietConversationEngine


class LLMProvider(ABC):
    """Abstract interface for an LLM provider."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        raise NotImplementedError


class FallbackLLMProvider(LLMProvider):
    """Deterministic provider used when no external LLM is configured."""

    def __init__(
        self,
        conversation_engine: DietConversationEngine,
        context: DietConversationContext,
    ) -> None:
        self.conversation_engine = conversation_engine
        self.context = context

    def generate(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        return self.conversation_engine.respond(
            user_message=user_message,
            context=self.context,
        )


class OpenAIProvider(LLMProvider):
    """OpenAI HTTP provider."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-mini",
    ) -> None:
        self.api_key = api_key
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    },
                ],
                "temperature": 0.3,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]


class DietLLMService:
    """Select the configured LLM provider with safe fallback."""

    def __init__(
        self,
        conversation_engine,
        context,
        api_key: str = "",
    ):
        self.conversation_engine = conversation_engine
        self.context = context
        self.api_key = api_key.strip()

    @property
    def llm_enabled(self) -> bool:
        return bool(self.api_key)

    def create_provider(self) -> LLMProvider:
        """
        Return OpenAI when configured,
        otherwise return the deterministic fallback provider.
        """

        if self.llm_enabled:
            return OpenAIProvider(
                api_key=self.api_key,
            )

        return FallbackLLMProvider(
            conversation_engine=self.conversation_engine,
            context=self.context,
        )