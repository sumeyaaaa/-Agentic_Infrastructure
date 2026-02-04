# Project Chimera - Dockerfile
# Status: Placeholder for Task 3.2

FROM python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -e ".[dev]"

# Copy application code (will be added in later tasks)
COPY . .

# Run tests by default
CMD ["make", "test"]

