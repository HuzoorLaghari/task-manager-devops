# Base Python image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy requirements first
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full app
COPY app /app

# Create database folder
RUN mkdir -p /app/database

# Expose Flask port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
