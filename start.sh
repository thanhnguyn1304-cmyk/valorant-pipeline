#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

# 1. Run database migrations
echo "Running database migrations..."
alembic upgrade head

# 2. Start Celery worker in the background
echo "Starting Celery worker..."
celery -A worker.celery_app worker --loglevel=info --concurrency=1 &

# 3. Start Uvicorn in the foreground
echo "Starting Uvicorn web server..."
# Using exec ensures uvicorn takes over the main process ID (PID 1)
# This is critical for Render to correctly detect the port binding
exec uvicorn main:app --host 0.0.0.0 --port $PORT
