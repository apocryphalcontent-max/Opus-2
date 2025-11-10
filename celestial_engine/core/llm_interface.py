"""
LLM interface for the Celestial Engine.
Handles communication with Ollama and model management.
"""

import requests
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from .config import get_config

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of models available."""
    PRIMARY = "primary"
    ADVANCED = "advanced"
    PREPROCESSOR = "preprocessor"
    VALIDATOR = "validator"


@dataclass
class GenerationRequest:
    """Request for text generation."""
    prompt: str
    model: str
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    num_ctx: int = 8192
    num_predict: int = -1
    stop: List[str] = None
    stream: bool = False


@dataclass
class GenerationResponse:
    """Response from text generation."""
    text: str
    model: str
    tokens_generated: int = 0
    generation_time: float = 0.0
    success: bool = True
    error: Optional[str] = None


class OllamaInterface:
    """Interface for communicating with Ollama."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """Initialize Ollama interface."""
        config = get_config()

        self.base_url = base_url or config.llm_base_url
        self.timeout = timeout or config.llm_timeout
        self.retry_attempts = config.llm_retry_attempts

        # Ensure base_url doesn't end with /
        self.base_url = self.base_url.rstrip('/')

        logger.info(f"Ollama interface initialized: {self.base_url}")

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        """
        Generate text using Ollama.

        Args:
            request: Generation request parameters

        Returns:
            Generation response with generated text
        """
        start_time = time.time()

        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": request.stream,
            "options": {
                "temperature": request.temperature,
                "top_p": request.top_p,
                "top_k": request.top_k,
                "repeat_penalty": request.repeat_penalty,
                "num_ctx": request.num_ctx,
                "num_predict": request.num_predict,
            }
        }

        if request.stop:
            payload["options"]["stop"] = request.stop

        # Try with retries
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=self.timeout
                )

                response.raise_for_status()
                result = response.json()

                generation_time = time.time() - start_time

                return GenerationResponse(
                    text=result.get("response", ""),
                    model=request.model,
                    tokens_generated=result.get("eval_count", 0),
                    generation_time=generation_time,
                    success=True,
                    error=None
                )

            except requests.exceptions.RequestException as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")

                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    generation_time = time.time() - start_time
                    return GenerationResponse(
                        text="",
                        model=request.model,
                        tokens_generated=0,
                        generation_time=generation_time,
                        success=False,
                        error=str(e)
                    )

    def generate_with_model_type(
        self,
        prompt: str,
        model_type: ModelType,
        **kwargs
    ) -> GenerationResponse:
        """
        Generate text using a specific model type.

        Args:
            prompt: Text prompt
            model_type: Type of model to use
            **kwargs: Additional generation parameters

        Returns:
            Generation response
        """
        config = get_config()
        model_config = config.get_model_config(model_type.value)

        if not model_config:
            logger.error(f"Model type '{model_type.value}' not found in configuration")
            return GenerationResponse(
                text="",
                model="unknown",
                success=False,
                error=f"Model type '{model_type.value}' not configured"
            )

        # Merge model config params with kwargs
        params = model_config.params.copy()
        params.update(kwargs)

        request = GenerationRequest(
            prompt=prompt,
            model=model_config.name,
            temperature=params.get("temperature", 0.7),
            top_p=params.get("top_p", 0.9),
            top_k=params.get("top_k", 40),
            repeat_penalty=params.get("repeat_penalty", 1.1),
            num_ctx=params.get("num_ctx", 8192),
            num_predict=params.get("num_predict", -1),
            stop=params.get("stop"),
            stream=params.get("stream", False)
        )

        logger.info(f"Generating with {model_config.name} ({model_type.value})")
        return self.generate(request)

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models in Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("models", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama library.

        Args:
            model_name: Name of model to pull

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Pulling model: {model_name}")

            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=3600  # 1 hour timeout for pulling
            )

            response.raise_for_status()
            logger.info(f"Successfully pulled model: {model_name}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False

    def check_model_available(self, model_name: str) -> bool:
        """Check if a model is available."""
        models = self.list_models()
        return any(m.get("name") == model_name for m in models)

    def warm_up_model(self, model_type: ModelType) -> bool:
        """
        Warm up a model by sending a test prompt.

        Args:
            model_type: Type of model to warm up

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Warming up {model_type.value} model")

        response = self.generate_with_model_type(
            prompt="Hello, this is a warmup prompt.",
            model_type=model_type
        )

        if response.success:
            logger.info(f"Model {model_type.value} warmed up successfully")
            return True
        else:
            logger.warning(f"Failed to warm up {model_type.value} model: {response.error}")
            return False

    def verify_setup(self) -> Dict[str, Any]:
        """
        Verify Ollama setup and model availability.

        Returns:
            Dictionary with verification results
        """
        results = {
            "ollama_running": False,
            "models_available": {},
            "all_ready": False
        }

        # Check if Ollama is running
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            results["ollama_running"] = True
        except requests.exceptions.RequestException:
            logger.error("Ollama is not running or not accessible")
            return results

        # Check each required model
        config = get_config()
        for model_type in [ModelType.PRIMARY, ModelType.ADVANCED, ModelType.PREPROCESSOR, ModelType.VALIDATOR]:
            model_config = config.get_model_config(model_type.value)
            if model_config:
                available = self.check_model_available(model_config.name)
                results["models_available"][model_type.value] = {
                    "name": model_config.name,
                    "available": available
                }

        # Check if all required models are available
        results["all_ready"] = (
            results["ollama_running"] and
            all(m["available"] for m in results["models_available"].values())
        )

        return results


# Global LLM interface instance
_global_llm: Optional[OllamaInterface] = None


def get_llm() -> OllamaInterface:
    """Get global LLM interface instance."""
    global _global_llm

    if _global_llm is None:
        _global_llm = OllamaInterface()

    return _global_llm
