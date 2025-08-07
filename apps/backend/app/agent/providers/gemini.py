import os
import logging
from typing import Any, Dict

import google.generativeai as genai
from fastapi.concurrency import run_in_threadpool

from ..exceptions import ProviderError
from .base import Provider, EmbeddingProvider
from ...core import settings

logger = logging.getLogger(__name__)


class GeminiProvider(Provider):
    def __init__(self, api_key: str | None = None, model_name: str = settings.LL_MODEL,
                 opts: Dict[str, Any] = None):
        if opts is None:
            opts = {}
        
        api_key = api_key or settings.GEMINI_API_KEY or settings.LLM_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ProviderError("Gemini API key is missing")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Default to gemini-1.5-flash if no model specified or if using default
        if model_name == settings.LL_MODEL or not model_name:
            model_name = "gemini-1.5-flash"
        
        self.model_name = model_name
        self.opts = opts
        
        try:
            self._model = genai.GenerativeModel(model_name)
        except Exception as e:
            raise ProviderError(f"Failed to initialize Gemini model '{model_name}': {e}") from e

    def _generate_sync(self, prompt: str, options: Dict[str, Any]) -> str:
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=options.get("temperature", 0.0),
                top_p=options.get("top_p", 0.9),
                top_k=options.get("top_k", 40),
                max_output_tokens=options.get("max_tokens", 8192),
            )
            
            response = self._model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                raise ProviderError("Gemini returned empty response")
            
            return response.text
            
        except Exception as e:
            raise ProviderError(f"Gemini - error generating response: {e}") from e

    async def __call__(self, prompt: str, **generation_args: Any) -> str:
        # Merge opts with generation_args, with generation_args taking precedence
        options = {
            "temperature": self.opts.get("temperature", 0.0),
            "top_p": self.opts.get("top_p", 0.9),
            "top_k": self.opts.get("top_k", 40),
            "max_tokens": self.opts.get("max_tokens", 8192),
        }
        options.update(generation_args)
        
        return await run_in_threadpool(self._generate_sync, prompt, options)


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        api_key: str | None = None,
        embedding_model: str = settings.EMBEDDING_MODEL,
    ):
        api_key = api_key or settings.GEMINI_API_KEY or settings.EMBEDDING_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ProviderError("Gemini API key is missing")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Default to text-embedding-004 if no model specified or using default
        if embedding_model == settings.EMBEDDING_MODEL or not embedding_model:
            embedding_model = "models/text-embedding-004"
        
        self._model = embedding_model

    async def embed(self, text: str) -> list[float]:
        try:
            response = await run_in_threadpool(
                genai.embed_content,
                model=self._model,
                content=text,
                task_type="retrieval_document"
            )
            
            if not response or 'embedding' not in response:
                raise ProviderError("Gemini returned invalid embedding response")
            
            return response['embedding']
            
        except Exception as e:
            raise ProviderError(f"Gemini - error generating embedding: {e}") from e
