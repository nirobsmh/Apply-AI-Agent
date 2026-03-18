from fastapi import FastAPI
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Hacker!"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return {
        "resume_skills": ["Python", "Javascript"],
        "job_skills": ["Javascript"],
        "missing_skills": ["Python"],
        "match_score": 89,
        "resume_suggestions": [
            "Highlight backend API development experience more clearly.",
            "Add deployment or infrastructure-related experience if relevant.",
            "Tailor your project bullets to match the job description language."
        ],
        "cover_letter": (
            "Dear Hiring Team,\n\n"
            "I am excited to apply for this role. My background in Python, FastAPI, "
            "and full-stack development aligns well with the position requirements. "
            "I have worked on building scalable software products and enjoy solving "
            "practical engineering problems.\n\n"
            "I would welcome the opportunity to contribute my experience and continue "
            "growing in a strong engineering environment.\n\n"
            "Sincerely,\n"
            "Your Name"
        )
    }