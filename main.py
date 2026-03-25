from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse
from app.services.extractor import resume_extractor, job_extractor, resume_suggestions
from app.services.matcher import compute_match
from app.services.cover_letter import cover_letter_f
from app.services.pdf_parser import parse_pdf
from app.services.analyzer import run_analyzer
from app.schemas.response import CoverLetterResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello Hacker!"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        resume_response = resume_extractor(request.resume_text)
        print("resume_response: ", resume_response)
        job_response = job_extractor(request.job_description)
        print("job_response: ", job_response)
        common_skills, missing_skills, match_score = compute_match(resume_response.skills, job_response.skills)
        print("common_skills: ", common_skills)
        print("missing_skills: ", missing_skills)
        print("match_score: ", match_score)
        resume_suggestions_response = resume_suggestions(request.resume_text, request.job_description, resume_response.skills, missing_skills, match_score)
        print("resume_suggestions_response: ", resume_suggestions_response)
        cover_letter_response = cover_letter_f(request.resume_text, request.job_description)
        print("cover_letter_response: ", cover_letter_response)
        return {
            "resume_skills": resume_response.skills,
            "job_skills": job_response.skills,
            "missing_skills": missing_skills,
            "match_score": match_score,
            "resume_suggestions": resume_suggestions_response.suggestions,
            "cover_letter": cover_letter_response.cover_letter
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze_upload")
async def analyze_upload(resume_file: UploadFile = File(...), job_description: str = Form(...)) -> "CoverLetterResponse":
    try:
        file_bytes = await resume_file.read()
        resume_text = parse_pdf(file_bytes)
        return run_analyzer(resume_text, job_description)
    except Exception as e:
        return {"error": str(e)}
