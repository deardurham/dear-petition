release: python manage.py migrate
web: gunicorn config.wsgi:application
# worker: celery worker --app=dear_petition.taskapp --loglevel=info
