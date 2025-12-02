# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src

# Install dependencies using uv
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python"]