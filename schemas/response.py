from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]
    missing_skills: list[str]
    match_score: int
    resume_suggestions: list[str]
    cover_letter: str
