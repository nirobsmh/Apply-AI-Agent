from app.services.extractor import resume_extractor, job_extractor
from app.services.matcher import compute_match
from app.services.extractor import resume_suggestions
from app.services.cover_letter import cover_letter_f
from app.schemas.response import AnalyzeResponse
from app.schemas.response import CoverLetterResponse

def run_analyzer(resume_text: str, job_description: str) -> CoverLetterResponse:
    """Run the analyzer."""
    try:
        # resume_response = resume_extractor(resume_text)
        #job_response = job_extractor(job_description)
        #common_skills, missing_skills, match_score = compute_match(resume_response.skills, job_response.skills)
        #resume_suggestions_response = resume_suggestions(resume_text, job_description, resume_response.skills, missing_skills, match_score)
        cover_letter_response = cover_letter_f(resume_text, job_description)
        # return AnalyzeResponse(resume_response=resume_response, job_response=job_response, common_skills=common_skills, missing_skills=missing_skills, match_score=match_score, resume_suggestions_response=resume_suggestions_response, cover_letter_response=cover_letter_response)
        return CoverLetterResponse.model_validate(cover_letter_response)
    except Exception as e:
        print("Error in run_analyzer: ", e)
        return CoverLetterResponse(cover_letter="")
        # return AnalyzeResponse(resume_response=None, job_response=None, common_skills=None, missing_skills=None, match_score=None, resume_suggestions_response=None, cover_letter_response=None)