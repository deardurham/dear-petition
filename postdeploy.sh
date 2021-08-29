#!/bin/sh
set -e

>&2 echo "Running Migrations"
python manage.py migrate --noinput

echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('qatester', 'qatester@example.com', 'qatester')" | python manage.py shell
