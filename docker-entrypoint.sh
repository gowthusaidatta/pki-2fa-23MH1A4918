#!/bin/sh
set -e

echo "[ENTRYPOINT] Booting..."

mkdir -p /cron
mkdir -p /data

echo "[ENTRYPOINT] Starting cron..."
cron &

sleep 1

echo "[ENTRYPOINT] Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8080
