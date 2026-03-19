from fastapi import FastAPI
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.services.extractor import resume_extractor, job_extractor

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Hacker!"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    resume_response = resume_extractor(request.resume_text)
    job_response = job_extractor(request.job_description)
    print(resume_response)
    return {
        "resume_skills": resume_response.skills,
        "job_skills": job_response.skills,
        "missing_skills": [""],
        "match_score": 0,
        "resume_suggestions": [],
        "cover_letter": ""
    }