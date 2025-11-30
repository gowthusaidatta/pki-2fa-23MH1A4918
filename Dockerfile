# =======================
# Stage 1: Builder
# =======================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# =======================
# Stage 2: Runtime
# =======================
FROM python:3.11-slim

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install dependencies including curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata procps curl && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app files
COPY app/ /app/
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem
COPY encrypted_seed.txt /app/encrypted_seed.txt

# Cron folders
RUN mkdir -p /cron /data && chmod -R 777 /cron

# Configure crontab
RUN printf "SHELL=/bin/sh\nPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\n" \
    > /etc/crontab

RUN echo "* * * * * root cd /app && PYTHONPATH=/app /usr/local/bin/python3 /app/scripts/log_2fa_cron.py >> /cron/last_code.txt 2>&1" \
    >> /etc/crontab

RUN chmod 644 /etc/crontab

# Entrypoint permissions
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8080
CMD ["/app/docker-entrypoint.sh"]
