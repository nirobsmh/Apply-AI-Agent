from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_description: str = Field(..., min_length=10)