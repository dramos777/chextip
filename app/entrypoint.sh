#!/usr/bin/env bash

gunicorn --timeout 120 --access-logfile - --error-logfile - --chdir /app app:app --bind 0.0.0.0:5000 --workers 5
