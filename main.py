from fastapi import FastAPI
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.services.extractor import resume_extractor, job_extractor
from app.services.matcher import compute_match

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Hacker!"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        resume_response = resume_extractor(request.resume_text)
        job_response = job_extractor(request.job_description)
        common_skills, missing_skills, match_score = compute_match(resume_response.skills, job_response.skills)
        print(resume_response)
        return {
            "resume_skills": resume_response.skills,
            "job_skills": job_response.skills,
            "missing_skills": missing_skills,
            "match_score": match_score,
            "resume_suggestions": [],
            "cover_letter": ""
        }
    except Exception as e:
        return {"error": str(e)}