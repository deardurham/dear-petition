#!/bin/sh
set -e

>&2 echo "Running Migrations"
python manage.py migrate --noinput

>&2 echo "Running bootstrap-review-app"
python manage.py bootstrap-review-app
