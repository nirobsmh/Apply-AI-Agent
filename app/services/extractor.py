from app.schemas.response import SkillExtractionResponse
from app.schemas.request import AnalyzeRequest
from app.services.llm_service import load_prompt
from app.services.llm_service import call_llm


def resume_extractor(resume_text: str) -> SkillExtractionResponse:
    prompt = load_prompt("app/prompts/extract_resume.txt")
    response = call_llm(prompt, resume_text)
    return SkillExtractionResponse.model_validate_json(response)
