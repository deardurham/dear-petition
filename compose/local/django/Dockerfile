FROM python:3.8-slim as static_files

RUN set -ex \
    && BUILD_DEPS=" \
    curl \
    build-essential \
    zlib1g-dev \
    libpng-dev \
    pkg-config \
    libfontconfig1-dev \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS

# Install poppler pdftotext, based on xpdf3 (the old version)
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
    vim \
    wget \
    curl \
    git \
    libpq-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install pdftotext
RUN set -ex \
    && wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz \
    && tar -xvf xpdf-tools-linux-4.04.tar.gz \
    && cp xpdf-tools-linux-4.04/bin64/pdftotext /usr/local/bin/pdftotext-4.03

FROM alpine:3.12

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3 python3-dev py-pip musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  # ZeroMQ
  && apk add libzmq zeromq-dev \
  # Git
  && apk add git \
  # glibc compat for pdftotext binaries
  && apk add libc6-compat

RUN ln -s /usr/bin/python3 /usr/local/bin/python
RUN ln -s /usr/bin/pip3 /usr/local/bin/pip

COPY --from=static_files /usr/local/bin/pdftotext /usr/local/bin/pdftotext
COPY --from=static_files /usr/local/bin/pdftotext-4.03 /usr/local/bin/pdftotext-4.03

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip3 install -U pip
RUN pip3 install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY ./compose/local/django/start-jupyter /start-jupyter
RUN sed -i 's/\r//' /start-jupyter
RUN chmod +x /start-jupyter

# reduce image size by cleaning up the build packages
RUN apk del build-base musl-dev python3-dev zeromq-dev postgresql-dev

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
