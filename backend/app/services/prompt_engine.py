"""Core Prompt Optimization Engine for PromptCraft AI.

Handles intent classification, domain selection, contextual translation,
framework templating (CO-STAR/CRISPE), and Arabic directive injection.
"""

import time
import re
from typing import Tuple, Dict, Any
from backend.app.core.prompts import (
    SYSTEM_PROMPT_OPTIMIZER,
    MANDATORY_ARABIC_DIRECTIVE,
    DOMAINS,
)
from backend.app.schemas.prompt import (
    PromptOptimizeRequest,
    PromptOptimizeResponse,
    ExecutePromptRequest,
    ExecutePromptResponse,
)
from backend.app.services.llm_client import llm_client


class PromptEngine:
    """The central Prompt Engineering Middleware."""

    DOMAIN_KEYWORDS = {
        "software_engineering": [
            "كود", "برمج", "فلاتر", "بايثون", "جافا", "رياكت", "api", "backend", "frontend",
            "database", "قاعدة بيانات", "دالة", "خطأ", "error", "bug", "flutter", "python",
            "javascript", "typescript", "fastapi", "node", "sql", "github", "تطبيق", "موقع"
        ],
        "data_science_ai": [
            "بيانات", "ذكاء اصطناعي", "تعلم الة", "تعلم آلي", "موديل", "تدريب", "خوارزمية",
            "dataset", "machine learning", "deep learning", "neural", "pandas", "numpy", "تحليل"
        ],
        "cybersecurity": [
            "اختراق", "ثغرة", "أمن", "حماية", "تشفير", "cyber", "security", "firewall",
            "vulnerability", "auth", "token", "jwt", "owasp", "sql injection", "xss"
        ],
        "academic_research": [
            "بحث", "دراسة", "أطروحة", "رسالة", "منهجية", "جامعي", "علمي", "مراجع", "فرضية",
            "paper", "thesis", "methodology", "literature review", "تحكيم"
        ],
        "creative_writing": [
            "قصة", "سيناريو", "مقال", "إعلان", "تسويق", "شعر", "بوست", "محتوى", "مدونة",
            "story", "copywriting", "creative", "narrative"
        ]
    }

    def detect_domain(self, text: str) -> str:
        """Classify user intent using domain keyword density with fallback to 'software_engineering' or 'general'."""
        text_lower = text.lower()
        scores: Dict[str, int] = {domain: 0 for domain in self.DOMAIN_KEYWORDS}

        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[domain] += 1

        top_domain = max(scores, key=scores.get)
        if scores[top_domain] > 0:
            return top_domain

        return "general"

    async def optimize(self, request: PromptOptimizeRequest) -> PromptOptimizeResponse:
        start_time = time.time()

        # 1. Domain Detection
        if not request.domain or request.domain == "auto":
            domain_id = self.detect_domain(request.prompt)
        else:
            domain_id = request.domain if request.domain in DOMAINS else "general"

        domain_meta = DOMAINS.get(domain_id, DOMAINS["general"])
        framework = request.framework or "CO-STAR"

        # 2. Build User Instruction for Optimizer LLM
        framework_instruction = (
            f"Apply the {framework} framework.\n"
            f"Target Domain: {domain_meta['name_en']}.\n"
            f"Target Persona: {domain_meta['persona']}\n"
            f"Quality Standards to emphasize:\n" + "\n".join(f"- {s}" for s in domain_meta["standards"]) + "\n"
            f"Default Format: {domain_meta['default_format']}\n"
        )

        user_content = (
            f"Please transform the following raw Arabic user prompt into a high-tier, professional English prompt.\n\n"
            f"--- ARABIC INPUT ---\n"
            f"{request.prompt}\n\n"
            f"--- CONFIGURATION ---\n"
            f"{framework_instruction}\n\n"
            f"Remember:\n"
            f"1. Zero conversational preamble. Return ONLY the final structured English prompt.\n"
            f"2. Conclude strictly with the MANDATORY ARABIC DIRECTIVE:\n"
            f"{MANDATORY_ARABIC_DIRECTIVE}"
        )

        # 3. Call LLM to generate the optimized prompt
        optimized_text = await llm_client.generate(
            prompt=user_content,
            system_instruction=SYSTEM_PROMPT_OPTIMIZER,
            provider=request.provider,
            temperature=request.temperature or 0.3
        )

        # 4. Guarantee Arabic Directive is present (Fail-safe injection)
        if "[LANGUAGE & RESPONSE DIRECTIVE]" not in optimized_text:
            optimized_text = f"{optimized_text.strip()}\n\n{MANDATORY_ARABIC_DIRECTIVE}"

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return PromptOptimizeResponse(
            original_prompt=request.prompt,
            detected_domain=domain_id,
            domain_name_ar=domain_meta["name_ar"],
            domain_name_en=domain_meta["name_en"],
            framework_used=framework,
            optimized_prompt=optimized_text,
            provider=request.provider or "default",
            processing_time_ms=elapsed_ms
        )

    async def execute_prompt(self, request: ExecutePromptRequest) -> ExecutePromptResponse:
        """Execute the optimized prompt against a target model to get the final answer."""
        start_time = time.time()

        result = await llm_client.generate(
            prompt=request.prompt,
            provider=request.provider,
            model=request.model,
            temperature=request.temperature or 0.7
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return ExecutePromptResponse(
            prompt=request.prompt,
            result=result,
            provider=request.provider or "default",
            model=request.model or "default",
            execution_time_ms=elapsed_ms
        )


prompt_engine = PromptEngine()
