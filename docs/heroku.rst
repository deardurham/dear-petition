
Heroku Setup
------------

First time::

    heroku apps:create --team dear dear-petition

Git Remote::

    heroku git:remote --app dear-petition

Provisioning::

    heroku stack --remote staging
    heroku stack:set heroku-18 --remote staging

    heroku buildpacks:clear --remote staging
    heroku buildpacks:add heroku/nodejs --remote staging
    heroku buildpacks:add heroku/python --remote staging
    heroku buildpacks:add https://github.com/carwow/heroku-buildpack-pdftotext.git --remote staging

    heroku addons:create heroku-postgresql:hobby-dev --remote staging
    heroku addons:create heroku-redis:hobby-dev --remote staging
    heroku addons:create mailgun:starter --remote staging

Environment variables::

    heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production --remote staging
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)" --remote staging
    heroku config:set DJANGO_ADMIN_URL="admin-$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 8)/" --remote staging
    heroku config:set DJANGO_AWS_ACCESS_KEY_ID="" --remote staging
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY="" --remote staging
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME="dear-petition-staging" --remote staging
    heroku config:set DJANGO_AWS_S3_REGION_NAME="us-east-1" --remote staging
    heroku config:set SENTRY_DSN="" --remote staging
    heroku config:set DJANGO_ALLOWED_HOSTS=dear-petition-staging.herokuapp.com --remote staging
    heroku config:set DJANGO_DEBUG=1 --remote staging
    heroku config:set DJANGO_SECURE_SSL_REDIRECT=0 --remote staging
    heroku config:set CELERY_BROKER_URL="" --remote staging
    heroku config:set CIPRS_READER_SOURCE="true" --remote staging

Deployment::

    git push heroku master
    # Example alt branch
    git push heroku deploy:master

Dev Ops::

    heroku logs --tail
    heroku run python manage.py createsuperuser
    heroku run python manage.py check --deploy
    heroku open

Setup scheduled DB backups::

    heroku pg:backups:schedule DATABASE_URL --at '02:00 America/New_York' --app dear-petition


Maintenance
-----------

View DB backups::

    heroku pg:backups --app dear-petition

Capture a DB backup now::

    heroku pg:backups:capture --app dear-petition
