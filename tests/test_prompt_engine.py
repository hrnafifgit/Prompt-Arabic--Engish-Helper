"""Unit and Benchmark Tests for PromptCraft AI Core Engine."""

import pytest
import asyncio
from backend.app.services.prompt_engine import prompt_engine
from backend.app.schemas.prompt import PromptOptimizeRequest


@pytest.mark.asyncio
async def test_domain_detection_software():
    prompt = "سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف"
    detected = prompt_engine.detect_domain(prompt)
    assert detected == "software_engineering", f"Expected software_engineering, got {detected}"


@pytest.mark.asyncio
async def test_domain_detection_ai():
    prompt = "اريد بناء موديل تعلم عميق لتصنيف بيانات الصور باستخدام بايتورش"
    detected = prompt_engine.detect_domain(prompt)
    assert detected == "data_science_ai", f"Expected data_science_ai, got {detected}"


@pytest.mark.asyncio
async def test_domain_detection_security():
    prompt = "كيف احمي مسارات الـ api من هجمات الحقن وثغرات sql injection"
    detected = prompt_engine.detect_domain(prompt)
    assert detected == "cybersecurity", f"Expected cybersecurity, got {detected}"


@pytest.mark.asyncio
async def test_domain_detection_academic():
    prompt = "اريد صياغة مشكلة البحث والمنهجية لدراسة جامعية حول نظم التوصية"
    detected = prompt_engine.detect_domain(prompt)
    assert detected == "academic_research", f"Expected academic_research, got {detected}"


@pytest.mark.asyncio
async def test_prompt_optimization_structure():
    request = PromptOptimizeRequest(
        prompt="سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف",
        domain="auto",
        framework="CO-STAR",
        provider="mock"
    )
    response = await prompt_engine.optimize(request)

    assert response.detected_domain == "software_engineering"
    assert response.framework_used == "CO-STAR"
    # Mandatory Arabic Directive MUST be present
    assert "[LANGUAGE & RESPONSE DIRECTIVE]" in response.optimized_prompt
    assert "CRITICAL INSTRUCTION FOR THE LLM" in response.optimized_prompt
    assert response.processing_time_ms >= 0


if __name__ == "__main__":
    asyncio.run(test_domain_detection_software())
    asyncio.run(test_domain_detection_ai())
    asyncio.run(test_domain_detection_security())
    asyncio.run(test_domain_detection_academic())
    asyncio.run(test_prompt_optimization_structure())
    print("✅ All PromptCraft AI unit tests passed successfully!")
