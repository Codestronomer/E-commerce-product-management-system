#!/usr/bin/env bash
# Exit on Error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migration
python manage.py migrate