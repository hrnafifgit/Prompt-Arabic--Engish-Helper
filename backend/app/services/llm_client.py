"""Multi-provider LLM Client supporting Google Gemini REST API, OpenAI, and a Smart Fallback."""

import logging
from typing import Optional, List
import httpx
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified LLM Client abstraction with direct REST and fail-safe handling."""

    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.gemini_models: List[str] = [
            settings.GEMINI_MODEL,
            "gemini-3.5-flash-lite",
            "gemini-flash-latest",
            "gemini-3.8-flash"
        ]

    async def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3
    ) -> str:
        provider = (provider or settings.DEFAULT_OPTIMIZER_PROVIDER).lower()

        # 1. Google Gemini via direct Async REST API
        if provider == "gemini":
            if self.gemini_key and len(self.gemini_key) > 10:
                try:
                    result = await self._call_gemini_rest(
                        prompt=prompt,
                        system_instruction=system_instruction,
                        preferred_model=model or settings.GEMINI_MODEL,
                        temperature=temperature
                    )
                    if result:
                        return result
                except Exception as e:
                    logger.warning(f"Gemini API request failed or timed out: {e}. Falling back to Smart Engine.")

            return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

        # 2. OpenAI
        if provider == "openai":
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                try:
                    return await self._call_openai(
                        prompt=prompt,
                        system_instruction=system_instruction,
                        model_name=model or settings.OPENAI_MODEL,
                        temperature=temperature
                    )
                except Exception as e:
                    logger.warning(f"OpenAI API call failed: {e}")

            return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

        # 3. Default Mock Provider
        return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

    async def _call_gemini_rest(
        self,
        prompt: str,
        system_instruction: Optional[str],
        preferred_model: str,
        temperature: float
    ) -> Optional[str]:
        models_to_try = [preferred_model] + [m for m in self.gemini_models if m != preferred_model]

        full_prompt = prompt
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n[USER INPUT]:\n{prompt}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 3000
            }
        }

        async with httpx.AsyncClient(timeout=25.0) as client:
            for model_name in models_to_try:
                clean_name = model_name.replace("models/", "")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_name}:generateContent?key={self.gemini_key}"
                try:
                    response = await client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            if parts:
                                return parts[0].get("text", "").strip()
                    elif response.status_code in (404, 503):
                        logger.info(f"Model {clean_name} returned {response.status_code}, trying next model...")
                        continue
                    else:
                        logger.warning(f"Gemini API returned status {response.status_code}: {response.text[:150]}")
                except httpx.TimeoutException:
                    logger.warning(f"Timeout calling Gemini {clean_name}")
                except Exception as err:
                    logger.warning(f"Error calling {clean_name}: {err}")

        return None

    async def _call_openai(
        self,
        prompt: str,
        system_instruction: Optional[str],
        model_name: str,
        temperature: float
    ) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def _mock_generate(self, prompt: str, system_instruction: Optional[str]) -> str:
        """Robust Heuristic Generator when offline or in fallback mode."""
        return (
            "[ROLE & PERSONA]\n"
            "Act as a Senior Technical Lead and Expert Architect.\n\n"
            "[CONTEXT]\n"
            f"The user has submitted the following requirement in Arabic: \"{prompt}\"\n\n"
            "[TASK]\n"
            "1. Comprehensively analyze the user's intent and architectural constraints.\n"
            "2. Provide a robust, production-grade implementation with zero compromises.\n"
            "3. Account for edge cases, error recovery, and security best practices.\n\n"
            "[CONSTRAINTS & QUALITY STANDARDS]\n"
            "- Ensure all code, imports, commands, and variables are written in standard English.\n"
            "- Adhere to idiomatic paradigms and clean architecture patterns.\n\n"
            "[OUTPUT FORMAT]\n"
            "Deliver an annotated, complete solution followed by an architectural summary.\n\n"
            "[LANGUAGE & RESPONSE DIRECTIVE]\n"
            "CRITICAL INSTRUCTION FOR THE LLM: \n"
            "Analyze, reason, and process the task using your full English technical capability. "
            "However, write your entire final output and response in clear, fluent, professional Arabic. "
            "Keep all code blocks, commands, technical terms, and variable names in standard English."
        )


llm_client = LLMClient()
