import logging
from typing import Any, List, Optional
import ollama
from chatbot.EboChatBotV1.config import AppConfig

config = AppConfig()

class OllamaLLM:
    model: str = config.OLLAMA_MODEL
    temperature: float = config.OLLAMA_TEMPERATURE

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        try:
            response = ollama.chat(model=self.model, messages=messages, stream=False)
            output = response.get("message", {}).get("content", "No response from model")
            logging.info("Ollama response: %s", output)
            return output
        except Exception as e:
            logging.exception("Error calling Ollama:")
            return f"Error: {e}"