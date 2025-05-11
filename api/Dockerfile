FROM python:3.10.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python source code
COPY src/ /app/src/
COPY api/ /app/api/
COPY pyproject.toml /app/

# Install the iq-puzzler package
RUN pip install -e .

# Create necessary directories for data
RUN mkdir -p /app/puzzle_vis/public/data/temp

# Copy any necessary data files
COPY puzzle_vis/public/data/*.json /app/puzzle_vis/public/data/

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8080

# Run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "2", "--timeout", "120", "api.app:app"]
