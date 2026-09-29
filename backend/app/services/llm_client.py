"""Multi-provider LLM Client supporting Google Gemini, OpenAI, and a Smart Mock Provider."""

import logging
from typing import Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified LLM Client abstraction."""

    def __init__(self):
        self._gemini_configured = False
        self._openai_client = None

        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._gemini_configured = True
            except Exception as e:
                logger.warning(f"Failed to configure Google Gemini: {e}")

        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                from openai import AsyncOpenAI
                self._openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to configure OpenAI: {e}")

    async def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3
    ) -> str:
        provider = (provider or settings.DEFAULT_OPTIMIZER_PROVIDER).lower()

        # 1. Google Gemini
        if provider == "gemini":
            if self._gemini_configured:
                return await self._call_gemini(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    model_name=model or settings.GEMINI_MODEL,
                    temperature=temperature
                )
            logger.info("Gemini API key not set or invalid, falling back to mock provider.")
            return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

        # 2. OpenAI
        if provider == "openai":
            if self._openai_client:
                return await self._call_openai(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    model_name=model or settings.OPENAI_MODEL,
                    temperature=temperature
                )
            logger.info("OpenAI API key not set, falling back to mock provider.")
            return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

        # 3. Default Mock Provider
        return self._mock_generate(prompt=prompt, system_instruction=system_instruction)

    async def _call_gemini(
        self,
        prompt: str,
        system_instruction: Optional[str],
        model_name: str,
        temperature: float
    ) -> str:
        import google.generativeai as genai
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=3000,
        )
        kwargs = {"generation_config": generation_config}
        if system_instruction:
            kwargs["system_instruction"] = system_instruction

        model = genai.GenerativeModel(model_name, **kwargs)
        # genai call in async-compatible thread
        response = await model.generate_content_async(prompt)
        return response.text.strip()

    async def _call_openai(
        self,
        prompt: str,
        system_instruction: Optional[str],
        model_name: str,
        temperature: float
    ) -> str:
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = await self._openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def _mock_generate(self, prompt: str, system_instruction: Optional[str]) -> str:
        """Heuristic mock response when no active API keys are supplied."""
        return (
            "[ROLE & PERSONA]\n"
            "Act as a Senior Technical Lead and Expert Consultant.\n\n"
            "[CONTEXT]\n"
            f"The user has submitted the following requirement in Arabic: \"{prompt}\"\n\n"
            "[TASK]\n"
            "1. Deeply decompose the core functional and technical requirements.\n"
            "2. Provide a robust, production-grade implementation with zero compromises.\n"
            "3. Account for edge cases, error recovery, and security best practices.\n\n"
            "[CONSTRAINTS & QUALITY STANDARDS]\n"
            "- Ensure all code, imports, and variables are written in standard English.\n"
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
