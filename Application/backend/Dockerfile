FROM python:3.12-slim

# =====================================================
# Python
# =====================================================

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# =====================================================
# Working Directory
# =====================================================

WORKDIR /app


# =====================================================
# System Dependencies
# =====================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*


# =====================================================
# Docker CLI
# =====================================================

RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*


# =====================================================
# Python Dependencies
# =====================================================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# =====================================================
# Application
# =====================================================

COPY . .


# =====================================================
# Backend Port
# =====================================================

EXPOSE 8000


# =====================================================
# Start FastAPI
# =====================================================

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]