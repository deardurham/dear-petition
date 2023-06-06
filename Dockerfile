FROM node:18-slim as dear_frontend

WORKDIR /code
ENV PATH /code/node_modules/.bin:$PATH
COPY package.json package-lock.json /code/
RUN npm install --silent
COPY index.html favicon.ico vite.config.js tailwind.config.js .postcssrc .eslintrc.json .eslintignore /code/
COPY ./src /code/src/

WORKDIR /code/

CMD ["npm", "run", "start"]

FROM dear_frontend as static_files

RUN npm run build

FROM python:3.8-slim-bullseye as base

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
#   libfontconfig -- required by pdftotext
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    libfontconfig \
    mime-support \
    postgresql-client \
    build-essential \
    xz-utils  \
    zlib1g-dev \
    libpng-dev \
    pkg-config \
    libfontconfig1-dev \
    vim \
    wget \
    curl \
    cmake \
    libfreetype6 \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install poppler pdftotext, based on xpdf3 (for parser mode V1)
RUN set -ex \
    && curl -k https://poppler.freedesktop.org/poppler-0.57.0.tar.xz | tar xJ \
    && chmod -R 755 ./poppler-0.57.0 \
    && cd ./poppler-0.57.0/ \
    && ./configure \
        --prefix=/tmp/poppler \
        --disable-shared \
        --enable-static \
        --enable-build-type=release \
        --enable-libopenjpeg=none \
        --enable-dctdecoder=none \
        --enable-shared=no \
    && make install \
    && cp /tmp/poppler/bin/pdftotext /usr/local/bin/pdftotext

# install xpdfreader pdftotext, which supports multiline description parsing
RUN set -ex \
    && curl -k https://dl.xpdfreader.com/xpdf-4.04.tar.gz | tar zxf - \
    && chmod -R 755 ./xpdf-4.04 \
    && cd ./xpdf-4.04/ \
    && mkdir build \
	&& cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_DISABLE_FIND_PACKAGE_Qt4=1 -DCMAKE_DISABLE_FIND_PACKAGE_Qt5Widgets=1 \
    && make \
    && cp xpdf/pdftotext /usr/local/bin/pdftotext-4

# Copy in your requirements file
# ADD requirements.txt /requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    git-core \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -r requirements/production.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY config/ /code/config/
COPY dear_petition/ /code/dear_petition/
COPY manage.py /code/manage.py
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
COPY postdeploy.sh /code/postdeploy.sh
# Silence missing .env notices
RUN touch /code/.env

FROM base AS deploy

# Copy in node-built files
COPY --from=static_files /code/build /code/build

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN SENDGRID_API_KEY='' DJANGO_ADMIN_URL='' SENTRY_DSN='' DATABASE_URL='' ENVIRONMENT='' DJANGO_SECRET_KEY='dummy' DOMAIN='' python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=config/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy UWSGI_IGNORE_SIGPIPE=true UWSGI_IGNORE_WRITE_ERRORS=true UWSGI_DISABLE_WRITE_EXCEPTION=true

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/staticfiles/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--http=0.0.0.0:$PORT", "--show-config"]

FROM base AS dev

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpq-dev \
    git-core \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements/local.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE=config.settings.local

ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
