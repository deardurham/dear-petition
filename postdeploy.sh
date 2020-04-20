#!/bin/sh
echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('qatester', 'qatester@example.com', 'qatester')" | python manage.py shell
