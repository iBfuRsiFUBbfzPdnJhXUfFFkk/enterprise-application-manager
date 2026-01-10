# Use Python 3.13 slim base (Debian-based for better compatibility)
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
# - poppler-utils: PDF processing (pdf2image)
# - gcc, build-essential: Compilation for native extensions
# - libldap2-dev, libsasl2-dev: LDAP support (if enabled)
# - curl: Health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    gcc \
    g++ \
    make \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MinIO dependencies
RUN pip install --no-cache-dir django-storages[s3] boto3

# Copy project
COPY . .

# Expose port 8000 (internal, nginx proxies to this)
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
