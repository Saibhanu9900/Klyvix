from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: float = Field(default_factory=lambda: 0.0)

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    session_id: Optional[str] = None
    file_ids: List[str] = []

class PersonaConfig(BaseModel):
    id: str
    display_name: str
    description: str
    system_prompt: str
    output_mode: Literal["freeform", "json_schema"]
    requires_upload: bool = False
    json_schema: Optional[Dict[str, Any]] = None

class CodeReviewIssue(BaseModel):
    issue: str
    location: str
    why_it_matters: str
    suggested_fix: str

class CodeReviewResponse(BaseModel):
    language_detected: str
    language_confidence: str
    bugs_and_correctness: List[CodeReviewIssue]
    security: List[CodeReviewIssue]
    performance: List[CodeReviewIssue]
    style_and_best_practices: List[CodeReviewIssue]
    summary: str
    overall_quality_rating: str

class ResumeSuggestion(BaseModel):
    original: str
    improved: str
    why: str

class ResumeReviewResponse(BaseModel):
    overall_assessment: str
    strengths: List[str]
    gaps: List[str]
    suggestions: List[ResumeSuggestion]
    priority_actions: List[str]

class DocumentUploadResponse(BaseModel):
    file_id: str
    filename: str
    total_chunks: int
    word_count: int
