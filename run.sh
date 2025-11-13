#!/usr/bin/env bash
# build and run locally (dev)
docker build -t mini-stats-api:latest .
docker run --rm -p 8080:8080 --env-file .env -v $(pwd)/assets:/app/assets mini-stats-api:latest

