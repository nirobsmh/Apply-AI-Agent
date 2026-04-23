from app.services.cover_letter import cover_letter_f
from app.schemas.response import CoverLetterResponse


def run_analyzer(resume_text: str, job_description: str) -> CoverLetterResponse:
    """Run the analyzer."""
    cover_letter_response = cover_letter_f(resume_text, job_description)
    return CoverLetterResponse.model_validate(cover_letter_response)
