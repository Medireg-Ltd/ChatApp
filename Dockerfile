# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to reduce Python's memory footprint
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django application code into the container
COPY . .

# Copy the entrypoint script into the container and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ensure the app can bind to the outside world on port 5000
EXPOSE 5000

# Set the entrypoint to run the migrations and start the server
ENTRYPOINT ["/entrypoint.sh"]