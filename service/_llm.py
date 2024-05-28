import asyncio

from llama_cpp import Llama

from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_llm_service import AbstractLLMService


class LLMService(AbstractLLMService):
    def __init__(self, config_service: AbstractConfig):
        super().__init__()
        self.config = config_service.get("llm")
        self._llm = Llama(
            model_path=self.config["model_path"],
            n_ctx=self.config["n_ctx"],
            n_threads=self.config["n_threads"],
            n_gpu_layers=self.config["n_gpu_layers"],
            n_batch=self.config["n_batch"],
            seed=1337,
            verbose=False,
        )
        self._lock = asyncio.Lock()

    async def call(self, system_prompt: str, user_prompt: str) -> str:
        async with self._lock:
            output = self._llm(
                f"<|system|>{system_prompt}<|end|><|user|>\n{user_prompt}<|end|>\n<|assistant|>",
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"],
                stop=["<|end|>"],
                stream=False,
                echo=False,
            )

            answer = output["choices"][0]["text"].strip()
            return answer
