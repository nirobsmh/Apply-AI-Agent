"""Extraction helpers for resume and job description text."""

from app.schemas.response import SkillExtractionResponse
from app.schemas.request import AnalyzeRequest
from app.services.llm_service import load_prompt
from app.services.llm_service import call_llm

def normalize_skills(skills: list[str]) -> list[str]:
    """Normalize a list of skills for consistent comparison."""
    skill_set = set(skills)
    for skill in skill_set:
        skill = skill.lower().strip()
    return list(skill_set)

def resume_extractor(resume_text: str) -> SkillExtractionResponse:
    """Extract skills from resume text using the LLM."""
    prompt = load_prompt("app/prompts/extract_resume.txt")
    response = call_llm(prompt, resume_text)
    print(response)
    response["skills"] = normalize_skills(response.get("skills", []))
    return SkillExtractionResponse.model_validate_json(response)

def job_extractor(job_description:str) -> SkillExtractionResponse:
    """Extract skills from a job description using the LLM."""
    prompt = load_prompt("app/prompts/extract_job.txt")
    response = call_llm(prompt, job_description)
    print(response)
    response["skills"] = normalize_skills(response.get("skills", []))
    return SkillExtractionResponse.model_validate_json(response)
