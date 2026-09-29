# Stage 1
FROM python:3.11-slim AS builder

WORKDIR /build

# Install 0S-level build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Optimize Layer Caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2
FROM python:3.11-slim AS runner

# Define non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -m -s /bin/bash appuser

WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .

# Ensure binaries are in the path for the non-root user
ENV PATH=/home/appuser/.local/bin:$PATH

ENTRYPOINT [ "python", "app.py" ]