# Dockerfile
# Build stage - compile dependencies
FROM python:3.11-slim as builder

# Set build-time environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies for psycopg2 and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
RUN mkdir /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Production stage - minimal runtime image
FROM python:3.11-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -r appuser && \
    mkdir -p /app/staticfiles /app/media/profile_pics /app/media/post_images && \
    chown -R appuser:appuser /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy application code with proper ownership
COPY --chown=appuser:appuser . .

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=blog_project.settings

# Switch to non-root user
USER appuser

# Collect static files (run as appuser)
RUN python manage.py collectstatic --noinput

# Expose application port
EXPOSE 8000



# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "blog_project.wsgi:application"]