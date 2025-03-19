#!/bin/bash

PORT="${PORT:-8887}"
uvicorn openmind.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload