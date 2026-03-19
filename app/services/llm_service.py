import json

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL

# client = OpenAI(api_key=OPENAI_API_KEY)
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def call_llm(prompt: str, input: str) -> dict:
    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=prompt,
        input=input,
    )
    return json.loads(response.output_text)
