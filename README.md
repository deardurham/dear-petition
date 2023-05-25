# DEAR Petition

A [Durham Expunction and Restoration (DEAR)](https://www.deardurham.org)
 project for creating petition forms.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Build Status](https://travis-ci.org/deardurham/dear-petition.svg?branch=master)](https://travis-ci.org/deardurham/dear-petition)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

- [DEAR Petition](#dear-petition)
  - [🚀 Docker Quick Start (recommended)](#-docker-quick-start-recommended)
  - [🐳 Development Container](#-development-container)
  - [Frontend Development](#frontend-development)
    - [🚀 Quick Setup](#-quick-setup)
    - [API Proxy Configuration](#api-proxy-configuration)
      - [Docker Container](#docker-container)
      - [Local Frontend](#local-frontend)
  - [Backend Development](#backend-development)
    - [Initial Setup](#initial-setup)
    - [Restore database](#restore-database)
    - [Configuring the containers using docker-compose.override.yml (optional)](#configuring-the-containers-using-docker-composeoverrideyml-optional)
  - [Development Tools and Testing](#development-tools-and-testing)
    - [Running tests with py.test](#running-tests-with-pytest)
    - [Test coverage](#test-coverage)
    - [Sign up for Sentry](#sign-up-for-sentry)
- [Production testing](#production-testing)

## 🚀 Docker Quick Start

```bash
git clone git@github.com:deardurham/dear-petition.git
cd dear-petition/
docker-compose up -d
docker-compose run --rm django python manage.py migrate
docker-compose run --rm django python manage.py createsuperuser
```

Try out DEAR Petition Generator by navigating to `http://localhost:3000`, logging in as the superuser you created, and uploading an example CIPRS pdf which can be downloaded from https://github.com/deardurham/ciprs-reader/tree/main/tests/test_records

## 🐳 Development Container

This project supports using a [Development Container](https://containers.dev/), is based on the [postgres](https://github.com/devcontainers/templates/tree/main/src/postgres) template and enables several features, including [python](https://github.com/devcontainers/features/tree/main/src/python) and [node](https://github.com/devcontainers/features/tree/main/src/node).

Before getting started, install [Visual Studio Code](https://code.visualstudio.com/) with the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension). See [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers) for additional information.

1. **Build and start dev container:** Using the [VS Code Command Pallete (`⇧⌘P`)](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette), select `Dev Containers: Reopen in Container`.
2. **Install Python and Node requirements:** 
   ```sh
   # Update pip
   python -m pip install --upgrade pip
   # Install Python packages
   pip install --user -r requirements/local.txt
   # Install node packages
   npm install
   ```
3. **Setup pre-commit:** Install pre-commit to enforce a variety of community standards:
   ```sh
   pre-commit clean
   pre-commit install
   ```
4. **Prepare your environment**: Run migrate and create a user for yourself:
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Start dev server:** Start the Django development server:
   ```sh
   python manage.py runserver
   ```
6. **Start Node dev server:** Start the Node development server in a separate terminal:
   ```sh
   npm run start
   ```

## Frontend Development

The user facing  side of the DEAR Petition Generator is a React single page app (SPA). It is common to run the frontend locally while running the backend on docker.


### 🚀 Quick Setup

```bash
docker compose up -d django # run the backend via docker in the background
npm i
npm run start
```


### API Proxy Configuration

The Petition Generator app uses a React frontend with a Django REST API backend. In the development environment, the React development server and Django backend will likely be hosted on different ports, and thus hosted on different urls. This causes issues when the frontend code sends API requests, such as a login request. The solution is to [proxy the API requests](https://create-react-app.dev/docs/proxying-api-requests-in-development/) to the url of the backend.

#### Docker Container

When the frontend is run using docker, the `API_PROXY` environment variable is set to `http://django:8000`.

You can override the this proxy url by setting `OVERRIDE_API_PROXY`:

```bash
OVERRIDE_API_PROXY=http://localhost:8888 docker-compose up -d
```

Note that there's an issue with the `node_modules` volume not updating when you add new dependencies. When this happens, run the following:

```bash
docker compose up --renew-anon-volumes -d frontend
```

#### Local Frontend

When using `npm run start` to run the frontend, the `API_PROXY` environment variable is unset. The fallback proxy is set to the `http://localhost:8000`.

You can set the proxy url by either setting `OVERRIDE_API_PROXY` or `API_PROXY`:

```bash
API_PROXY=http://localhost:8888 npm start
```

## Backend Development

### Initial Setup

To run this on a Mac, use [Docker for
Mac](https://docs.docker.com/docker-for-mac/install/).

Build the project containers:

    docker-compose build

Run the containers:

    docker-compose up -d django

Migrate DB:

    docker-compose run --rm django python manage.py migrate

Create a superuser:

    docker-compose run --rm django python manage.py createsuperuser

When asked for a username and password, enter values of your choosing.  Email address may be left empty.    

Visit http://localhost:8000/petition/api/ in your browser.  If you get authentication errors, you may login as the superuser you created at http://localhost:8000/ and try again.

See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


### Restore database

If you have a database dump you wish to restore, you can run:

```sh
docker-compose run --rm django sh
$ dropdb dear_petition
$ createdb dear_petition
$ pg_restore -Ox -d dear_petition latest.dump
$ python manage.py migrate
```

### Configuring the containers using docker-compose.override.yml (optional)

To develop in a Docker container, we'll create a `docker-compose.override.yml`
override file in the root of the `dear-petition` directory to configure the Django container to sleep by default:

```yaml
# file: docker-compose.override.yml
version: '3'

services:
  django:
    command: ["sleep", "infinity"]
```

Now we run `runserver` manually to have more control over restarts:

```sh
docker-compose up -d django
docker-compose exec django bash
root$ python manage.py runserver 0.0.0.0:8000
```

## Development Tools and Testing

### Running tests with py.test

    $ docker-compose run --rm django pytest
    
### Test coverage

Test coverage is automatically generated as part of `pytest`.

To manually run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

### Sign up for Sentry

The dear-petition project is now on Sentry. Visit sentry.io and make an account or sign in with Github. Reach out to an existing member for an invite to the project.


# Production testing

To test the production Dockerfile locally, run:

```sh
COMPOSE_FILE=docker-compose.deploy.yml docker compose up --build -d django
# View logs for debugging
COMPOSE_FILE=docker-compose.deploy.yml docker compose logs django -f
```
