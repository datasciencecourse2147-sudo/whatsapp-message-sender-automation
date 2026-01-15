# Use Python 3.11 slim base image
FROM python:3.11-slim

# Install Chromium and ChromeDriver (simpler than Chrome)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set display port to avoid crash
ENV DISPLAY=:99

# Set Chromium binary location
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p whatsapp_session uploads

# Expose port (Render uses PORT env variable)
EXPOSE 10000

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 300 send_msg:app