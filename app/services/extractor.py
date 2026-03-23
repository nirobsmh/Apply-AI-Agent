"""Extraction helpers for resume and job description text."""

from app.schemas.response import SkillExtractionResponse
from app.schemas.request import AnalyzeRequest
from app.services.llm_service import load_prompt
from app.services.llm_service import call_llm
from app.schemas.response import ResumeSuggestionsResponse

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
    return SkillExtractionResponse.model_validate(response)

def job_extractor(job_description:str) -> SkillExtractionResponse:
    """Extract skills from a job description using the LLM."""
    prompt = load_prompt("app/prompts/extract_job.txt")
    response = call_llm(prompt, job_description)
    print(response)
    response["skills"] = normalize_skills(response.get("skills", []))
    return SkillExtractionResponse.model_validate(response)

def resume_suggestions(resume_text: str, job_description: str, resume_skills: list[str], missing_skills: list[str], match_score: int) -> ResumeSuggestionsResponse:
    """Suggest resume improvements based on the resume, job description, resume skills, missing skills, and match score."""
    prompt = load_prompt("app/prompts/resume_suggestions.txt")
    inputText = "Resume text: " + resume_text + "\n\n" + "Job description: " + job_description + "\n\n" + "Resume skills: " + ", ".join(resume_skills) + "\n\n" + "Missing skills: " + ", ".join(missing_skills) + "\n\n" + "Match score: " + str(match_score)
    response = call_llm(prompt, inputText)
    print(response)
    return ResumeSuggestionsResponse.model_validate(response)
