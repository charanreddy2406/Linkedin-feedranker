FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir .
COPY src ./src
# A long-running consumer — no port, just the loop.
CMD ["python", "-m", "src.main"]
