# Get base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Run the FastAPI application when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
