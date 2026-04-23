import logging

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.schemas.request import AnalyzeRequest
from app.schemas.response import AnalyzeResponse, CoverLetterResponse
from app.services.analyzer import run_analyzer
from app.services.cover_letter import cover_letter_f
from app.services.extractor import job_extractor, resume_extractor, resume_suggestions
from app.services.llm_service import LLMRequestError, LLMResponseParseError
from app.services.matcher import compute_match
from app.services.pdf_parser import parse_pdf

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello Hacker!"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        resume_response = resume_extractor(request.resume_text)
        job_response = job_extractor(request.job_description)
        _, missing_skills, match_score = compute_match(
            resume_response.skills,
            job_response.skills,
        )
        resume_suggestions_response = resume_suggestions(
            request.resume_text,
            request.job_description,
            resume_response.skills,
            missing_skills,
            match_score,
        )
        cover_letter_response = cover_letter_f(
            request.resume_text,
            request.job_description,
        )
        return AnalyzeResponse(
            resume_skills=resume_response.skills,
            job_skills=job_response.skills,
            missing_skills=missing_skills,
            match_score=match_score,
            resume_suggestions=resume_suggestions_response.suggestions,
            cover_letter=cover_letter_response.cover_letter,
        )
    except (LLMRequestError, LLMResponseParseError, ValidationError) as exc:
        logger.exception("Failed to process /analyze due to LLM output.")
        raise HTTPException(
            status_code=502,
            detail="Failed to process response from language model.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error in /analyze.")
        raise HTTPException(status_code=500, detail="Internal server error.") from exc


def _is_pdf_upload(file: UploadFile) -> bool:
    content_type = (file.content_type or "").lower()
    filename = (file.filename or "").lower()
    return content_type == "application/pdf" or filename.endswith(".pdf")


@app.post("/analyze_upload")
async def analyze_upload(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
) -> CoverLetterResponse:
    cleaned_job_description = job_description.strip()
    if not cleaned_job_description:
        raise HTTPException(status_code=400, detail="job_description cannot be empty.")

    if not _is_pdf_upload(resume_file):
        raise HTTPException(status_code=400, detail="resume_file must be a PDF.")

    file_bytes = await resume_file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="resume_file is empty.")

    try:
        resume_text = parse_pdf(file_bytes)
    except Exception as exc:
        logger.exception("Failed to parse uploaded PDF.")
        raise HTTPException(status_code=400, detail="Unable to parse uploaded PDF.") from exc

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF does not contain readable text.",
        )

    try:
        return run_analyzer(resume_text, cleaned_job_description)
    except (LLMRequestError, LLMResponseParseError, ValidationError) as exc:
        logger.exception("Failed to process /analyze_upload due to LLM output.")
        raise HTTPException(
            status_code=502,
            detail="Failed to process response from language model.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error in /analyze_upload.")
        raise HTTPException(status_code=500, detail="Internal server error.") from exc
