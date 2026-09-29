"""API Endpoints for Prompt Optimization, Domain exploration, and LLM Execution."""

from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.prompt import (
    PromptOptimizeRequest,
    PromptOptimizeResponse,
    DomainsListResponse,
    DomainInfo,
    ExecutePromptRequest,
    ExecutePromptResponse,
)
from backend.app.core.prompts import DOMAINS
from backend.app.services.prompt_engine import prompt_engine

router = APIRouter(prefix="/prompt", tags=["Prompt Optimization"])


@router.post(
    "/optimize",
    response_model=PromptOptimizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Optimize Arabic prompt into English structured prompt"
)
async def optimize_prompt(request: PromptOptimizeRequest):
    """
    Ingests an Arabic prompt, recognizes its domain, contextually translates it,
    applies the requested framework (CO-STAR/CRISPE), and appends the mandatory Arabic response directive.
    """
    try:
        return await prompt_engine.optimize(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prompt optimization failed: {str(e)}"
        )


@router.post(
    "/execute",
    response_model=ExecutePromptResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute engineered prompt directly on target LLM"
)
async def execute_prompt(request: ExecutePromptRequest):
    """
    Sends an engineered prompt to the selected LLM and returns the Arabic response.
    """
    try:
        return await prompt_engine.execute_prompt(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prompt execution failed: {str(e)}"
        )


@router.get(
    "/domains",
    response_model=DomainsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List supported domains and personas"
)
async def get_domains():
    """Returns all supported domains, personas, and quality standards."""
    domain_list = [
        DomainInfo(
            id=d["id"],
            name_ar=d["name_ar"],
            name_en=d["name_en"],
            persona=d["persona"],
            standards=d["standards"],
            default_format=d["default_format"],
        )
        for d in DOMAINS.values()
    ]
    return DomainsListResponse(domains=domain_list)


@router.get(
    "/templates",
    status_code=status.HTTP_200_OK,
    summary="Get preset case studies and prompt templates"
)
async def get_templates():
    """Returns sample Arabic prompts and benchmark cases."""
    return [
        {
            "id": 1,
            "title_ar": "مصادقة فلاتر مع فايربيس برقم الهاتف",
            "domain": "software_engineering",
            "arabic_prompt": "سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف",
            "framework": "CO-STAR"
        },
        {
            "id": 2,
            "title_ar": "بناء شبكة عصبية لتصنيف الصور",
            "domain": "data_science_ai",
            "arabic_prompt": "اريد موديل بايتورش لتصنيف الصور باستخدام كود نظيف وتدريب على GPU",
            "framework": "CO-STAR"
        },
        {
            "id": 3,
            "title_ar": "تأمين واجهات الـ REST API بواسطة JWT",
            "domain": "cybersecurity",
            "arabic_prompt": "كيف أحمي مسارات الباك إند بواسطة توكن JWT وأمنع هجمات XSS و CSRF",
            "framework": "CRISPE"
        },
        {
            "id": 4,
            "title_ar": "صياغة مشكلة البحث وأهداف الدراسة",
            "domain": "academic_research",
            "arabic_prompt": "ساعدني في كتابة مشكلة البحث والمنهجية لدراسة تأثير الذكاء الاصطناعي في التعليم الجامعي",
            "framework": "CO-STAR"
        }
    ]
