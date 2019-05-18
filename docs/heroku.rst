
Heroku Setup
------------

First time::

    heroku apps:create --team dear dear-petition

Git Remote::

    heroku git:remote --app dear-petition

Provisioning::

    heroku stack
    # gave up on this one:
    # heroku stack:set container
    heroku stack:set heroku-18

    heroku addons:create heroku-postgresql:hobby-dev
    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun:starter

Environment variables::

    heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"
    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/"
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=""
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=""
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME="dear-petition-staging"
    heroku config:set SENTRY_DSN=""
    heroku config:set DJANGO_ALLOWED_HOSTS=dear-petition.herokuapp.com
    heroku config:set DJANGO_DEBUG=1
    heroku config:set DJANGO_SECURE_SSL_REDIRECT=0

Deployment::

    git push heroku master
    # Example alt branch
    git push heroku deploy:master

Dev Ops::

    heroku logs --tail
    heroku run python manage.py createsuperuser
    heroku run python manage.py check --deploy
    heroku open
