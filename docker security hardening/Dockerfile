# Stage 1: Build Stage
FROM python:3.11-slim AS builder
WORKDIR /build
# Install 0S-level build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Optimize Layer Caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Test Stage
FROM builder AS tester
WORKDIR /build
COPY test_app.py .
RUN python -m pytest

# Stage 3: Runtime Stage
FROM python:3.11-slim AS runner
# make a fake reference to run the tests
COPY --from=tester /tmp/dumm[y] /tmp/dummy
# Define non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -m -s /bin/bash appuser

WORKDIR /app
# Copy only the installed dependencies from the builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .
# Ensure binaries are in the path for the non-root user
ENV PATH=/home/appuser/.local/bin:$PATH

# TODO: Switch to the non-root user
USER appuser
# TODO: Expose the necessary port
EXPOSE 8080

# Run the FastAPI application when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]