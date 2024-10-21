#!/usr/bin/env bash

gunicorn --chdir /app app:app --bind 0.0.0.0:5000 --workers 3
