# Use the official Python 3.11 image as our base image.
FROM python:3.11-slim

# Create and switch to the working directory inside the container.
WORKDIR /app

# Copy only the dependency file first.
# This allows Docker to cache the dependency installation layer.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code.
COPY app.py .

# Start the application when the container launches.
# Uvicorn gets 25 seconds to complete active requests after SIGTERM.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "25"]
