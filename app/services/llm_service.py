import json
import logging
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class LLMRequestError(RuntimeError):
    """Raised when the LLM service request fails."""


class LLMResponseParseError(ValueError):
    """Raised when model output is not valid JSON for this app."""


# client = OpenAI(api_key=OPENAI_API_KEY)
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _strip_code_fences(text: str) -> str:
    """Allow model responses wrapped in markdown code fences."""
    cleaned = text.strip()
    if not cleaned.startswith("```"):
        return cleaned

    lines = cleaned.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def call_llm(prompt: str, input: str) -> dict[str, Any]:
    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=prompt,
            input=input,
        )
    except Exception as exc:
        logger.exception("LLM request failed.")
        raise LLMRequestError("Failed to get a response from the LLM service.") from exc

    output_text = _strip_code_fences(response.output_text or "")
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise LLMResponseParseError("LLM output is not valid JSON.") from exc

    if not isinstance(parsed, dict):
        raise LLMResponseParseError("LLM output must be a JSON object.")

    return parsed
