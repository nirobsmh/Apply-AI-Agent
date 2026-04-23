from app.schemas.response import CoverLetterResponse
from app.services.llm_service import load_prompt
from app.services.llm_service import call_llm


def cover_letter_f(resume_text: str, job_description: str) -> CoverLetterResponse:
    """Write a cover letter based on the resume and job description."""
    prompt = load_prompt("app/prompts/cover_letter.txt")
    inputText = "Resume text: " + resume_text + "\n\n" + "Job description: " + job_description
    response = call_llm(prompt, inputText)
    return CoverLetterResponse.model_validate(response)
