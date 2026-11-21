FROM python:3.12-slim

# uv for fast installs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. Install packages first (cached if code changes)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# 2. Copy code and PDFs
COPY src/ src/
COPY data/ data/

ENV PATH="/app/.venv/bin:$PATH" \
    OLLAMA_BASE_URL=http://host.docker.internal:11434 \
    RERANK_DEVICE=cpu \
    HF_HOME=/root/.cache/huggingface

EXPOSE 8000
CMD ["uvicorn", "api:api", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]