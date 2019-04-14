FROM alpine:3.9.3

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3 python3-dev musl-dev \
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
  && apk add git

RUN ln -s /usr/bin/python3 /usr/local/bin/python

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
