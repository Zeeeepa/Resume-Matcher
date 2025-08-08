import os
import json
import logging
from typing import Any, Dict
import httpx
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
        
        self.api_key = api_key or settings.GEMINI_API_KEY or settings.LLM_API_KEY or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ProviderError("Gemini API key is missing")
        
        # Use the model from settings if no specific model provided
        if not model_name:
            model_name = settings.LL_MODEL
        
        self.model_name = model_name
        self.opts = opts
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def __call__(self, prompt: str, **generation_args: Any) -> str:
        # Merge opts with generation_args
        options = {
            "temperature": self.opts.get("temperature", 0.0),
            "top_p": self.opts.get("top_p", 0.9),
            "top_k": self.opts.get("top_k", 40),
            "max_tokens": self.opts.get("max_tokens", 8192),
        }
        options.update(generation_args)
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": options["temperature"],
                "topP": options["top_p"],
                "topK": options["top_k"],
                "maxOutputTokens": options["max_tokens"]
            }
        }
        
        url = f"{self.base_url}/models/{self.model_name}:generateContent"
        
        # Debug logging
        logger.debug(f"Making request to URL: {url}")
        logger.debug(f"API key present: {'Yes' if self.api_key else 'No'}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    params={"key": self.api_key},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    return content
                else:
                    raise ProviderError("No response from Gemini API")
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP {e.response.status_code}: {e.response.text}")
                raise ProviderError(f"Gemini API HTTP {e.response.status_code}: {e.response.text}")
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                raise ProviderError(f"Gemini API request error: {e}")
            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                raise ProviderError(f"Gemini API error: {e}")


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str | None = None, embedding_model: str = settings.EMBEDDING_MODEL):
        self.api_key = api_key or settings.GEMINI_API_KEY or settings.EMBEDDING_API_KEY or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ProviderError("Gemini API key is missing")
        
        # Default to text-embedding-004 if no model specified
        if embedding_model == settings.EMBEDDING_MODEL or not embedding_model:
            embedding_model = "text-embedding-004"
        
        # Ensure model name doesn't have "models/" prefix for URL construction
        if embedding_model.startswith("models/"):
            embedding_model = embedding_model[7:]  # Remove "models/" prefix
        
        self._model = embedding_model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def embed(self, text: str) -> list[float]:
        payload = {
            "model": f"models/{self._model}",
            "content": {"parts": [{"text": text}]},
            "taskType": "RETRIEVAL_DOCUMENT"
        }
        
        url = f"{self.base_url}/models/{self._model}:embedContent"
        
        # Debug logging
        logger.debug(f"Making embedding request to URL: {url}")
        logger.debug(f"API key present: {'Yes' if self.api_key else 'No'}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    params={"key": self.api_key},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                data = response.json()
                if "embedding" in data and "values" in data["embedding"]:
                    return data["embedding"]["values"]
                else:
                    raise ProviderError("Invalid embedding response from Gemini")
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP {e.response.status_code}: {e.response.text}")
                raise ProviderError(f"Gemini embedding HTTP {e.response.status_code}: {e.response.text}")
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                raise ProviderError(f"Gemini embedding request error: {e}")
            except Exception as e:
                logger.error(f"Gemini embedding error: {e}")
                raise ProviderError(f"Gemini embedding error: {e}")
