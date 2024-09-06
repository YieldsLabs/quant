import asyncio
from typing import Any, Dict

from llama_cpp import Llama

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_llm_service import AbstractLLMService


class LLMService(AbstractLLMService):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("copilot")
        self._llm = self._initialize_llm(self.config)
        self._lock = asyncio.Semaphore(3)

    async def call(
        self, system_prompt: str, user_prompt: str, stop_words: tuple[str] = ("<|end|>")
    ) -> str:
        async with self._lock:
            llama_input = {
                "prompt": f"<|system|>{system_prompt}<|end|><|user|>\n{user_prompt}<|end|>\n<|assistant|>",
                "max_tokens": self.config["max_tokens"],
                "temperature": self.config["temperature"],
                "stop": list(stop_words),
                "stream": True,
                "echo": False,
            }

            answer = ""

            for output in self._llm(**llama_input):
                answer += output["choices"][0]["text"]

            return answer

    @staticmethod
    def _initialize_llm(config: Dict[str, Any]) -> Llama:
        return Llama(
            model_path=config["model_path"],
            n_ctx=config["n_ctx"],
            n_threads=config["n_threads"],
            n_gpu_layers=config["n_gpu_layers"],
            n_batch=config["n_batch"],
            seed=1337,
            verbose=False,
        )
