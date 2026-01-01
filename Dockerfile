# Use an official Python image
FROM python:3.13-slim

# Install system dependencies needed by Playwright and Chromium
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libxfixes3 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and Chromium
RUN pip install --no-cache-dir playwright
RUN playwright install chromium

# Copy the rest of the code
COPY . .

# Run the main script
CMD ["python", "-u", "main.py", "render"]

