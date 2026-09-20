from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from app.core.config import settings
import os


class BaseAgent(ABC):
    _warmup_done = False
    _mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
    
    def __init__(self, llm: Optional[BaseChatModel] = None):
        self.llm = llm or self._get_default_llm()
    
    def _get_default_llm(self) -> BaseChatModel:
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.1,
            num_predict=800,
            timeout=600,
        )
    
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def _format_prompt(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)
    
    async def warmup(self) -> bool:
        """Warm up the model by making a test call"""
        if self._mock_mode:
            return True
        if BaseAgent._warmup_done:
            return True
        try:
            await self.llm.ainvoke("Say 'ready'")
            BaseAgent._warmup_done = True
            return True
        except Exception:
            return False