#!/bin/sh
set -e

>&2 echo "Running docker-entrypoint.sh"

if [ "x$DATABASE_CHECK_CONNECTION" = 'xon' ]; then
    until psql $DATABASE_URL -c '\l'; do
        >&2 echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Postgres is up - continuing"
fi

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    >&2 echo "Running Migrations"
    python manage.py migrate --noinput
fi

exec "$@"
