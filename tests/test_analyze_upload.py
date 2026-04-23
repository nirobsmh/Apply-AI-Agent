import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.response import CoverLetterResponse
from app.services.llm_service import LLMResponseParseError
from main import app


class AnalyzeUploadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_analyze_upload_success(self) -> None:
        with patch("main.parse_pdf", return_value="Resume text"), patch(
            "main.run_analyzer",
            return_value=CoverLetterResponse(cover_letter="Generated cover letter"),
        ):
            response = self.client.post(
                "/analyze_upload",
                files={"resume_file": ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")},
                data={"job_description": "Backend engineer role with Python and FastAPI"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"cover_letter": "Generated cover letter"})

    def test_analyze_upload_missing_job_description(self) -> None:
        response = self.client.post(
            "/analyze_upload",
            files={"resume_file": ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")},
        )
        self.assertEqual(response.status_code, 422)

    def test_analyze_upload_empty_job_description(self) -> None:
        response = self.client.post(
            "/analyze_upload",
            files={"resume_file": ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")},
            data={"job_description": "   "},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "job_description cannot be empty.")

    def test_analyze_upload_missing_resume_file(self) -> None:
        response = self.client.post(
            "/analyze_upload",
            data={"job_description": "Backend engineer role with Python and FastAPI"},
        )
        self.assertEqual(response.status_code, 422)

    def test_analyze_upload_invalid_file_type(self) -> None:
        response = self.client.post(
            "/analyze_upload",
            files={"resume_file": ("resume.txt", b"not a pdf", "text/plain")},
            data={"job_description": "Backend engineer role with Python and FastAPI"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "resume_file must be a PDF.")

    def test_analyze_upload_empty_file(self) -> None:
        response = self.client.post(
            "/analyze_upload",
            files={"resume_file": ("resume.pdf", b"", "application/pdf")},
            data={"job_description": "Backend engineer role with Python and FastAPI"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "resume_file is empty.")

    def test_analyze_upload_llm_parse_error_returns_502(self) -> None:
        with patch("main.parse_pdf", return_value="Resume text"), patch(
            "main.run_analyzer",
            side_effect=LLMResponseParseError("Bad JSON output"),
        ):
            response = self.client.post(
                "/analyze_upload",
                files={"resume_file": ("resume.pdf", b"%PDF-1.4 fake", "application/pdf")},
                data={"job_description": "Backend engineer role with Python and FastAPI"},
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json()["detail"],
            "Failed to process response from language model.",
        )


if __name__ == "__main__":
    unittest.main()
