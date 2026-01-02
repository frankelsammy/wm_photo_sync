FROM python:3.13-slim

ENV TZ=America/New_York

# System deps for Playwright / Chromium
RUN apt-get update && apt-get install -y \
    tzdata \
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

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir playwright \
    && playwright install chromium

COPY . .

CMD ["python", "-u", "main.py", "render"]
