FROM python:3.11-slim

# Set environment variables for unbuffered output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* ./
COPY main.py ./
COPY .env ./

RUN uv sync --frozen

CMD ["uv", "run", "python", "main.py"]
