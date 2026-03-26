## Getting Started

First, run the llm model with ollama or you can use OpenAI API:

```bash
ollama run deepseek-r1:latest
```

run backend
```bash
source .venv/bin/activate

python -m uvicorn main:app --reload
#or
fastapi dev
```
Backend will run at [http://127.0.0.1:8000](http://127.0.0.1:8000)

run frontend
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
