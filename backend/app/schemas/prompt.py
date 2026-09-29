"""Pydantic schemas for Prompt Optimization and LLM Execution."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PromptOptimizeRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=2,
        description="The raw prompt in Arabic (simple, conversational, or technical)."
    )
    domain: Optional[str] = Field(
        default="auto",
        description="Domain identifier (e.g. software_engineering, data_science_ai) or 'auto' for automatic intent detection."
    )
    framework: Optional[str] = Field(
        default="CO-STAR",
        description="Prompt engineering framework: 'CO-STAR' or 'CRISPE'."
    )
    provider: Optional[str] = Field(
        default=None,
        description="LLM provider for optimization ('gemini', 'openai', 'mock'). Defaults to configured default."
    )
    temperature: Optional[float] = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Temperature for generation (lower is more deterministic and structured)."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "سوي لي كود فلاتر يربط مع الفايربيس للتحقق من هوية المستخدم برقم الهاتف",
                "domain": "auto",
                "framework": "CO-STAR"
            }
        }


class PromptOptimizeResponse(BaseModel):
    original_prompt: str
    detected_domain: str
    domain_name_ar: str
    domain_name_en: str
    framework_used: str
    optimized_prompt: str
    provider: str
    processing_time_ms: float


class DomainInfo(BaseModel):
    id: str
    name_ar: str
    name_en: str
    persona: str
    standards: List[str]
    default_format: str


class DomainsListResponse(BaseModel):
    domains: List[DomainInfo]


class ExecutePromptRequest(BaseModel):
    prompt: str = Field(..., min_length=2, description="The engineered prompt to send to the target model.")
    provider: Optional[str] = Field(default=None, description="LLM provider: 'gemini', 'openai', 'mock'.")
    model: Optional[str] = Field(default=None, description="Specific target model name.")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.5)


class ExecutePromptResponse(BaseModel):
    prompt: str
    result: str
    provider: str
    model: str
    execution_time_ms: float
