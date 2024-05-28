from abc import ABC, abstractmethod


class AbstractLLMService(ABC):
    @abstractmethod
    def call(self, system_prompt: str, user_prompt: str) -> str:
        pass
