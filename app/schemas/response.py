from pydantic import BaseModel

class SkillExtractionResponse(BaseModel):
    skills: list[str]

class ResumeSuggestionsResponse(BaseModel):
    suggestions: list[str]

class CoverLetterResponse(BaseModel):
    cover_letter: str     

class AnalyzeResponse(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]
    missing_skills: list[str]
    match_score: int
    resume_suggestions: list[str]
    cover_letter: str
