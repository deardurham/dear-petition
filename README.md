# DEAR Petition

A [Durham Expunction and Restoration (DEAR)](https://www.deardurham.org)
 project for creating petition forms.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Build Status](https://travis-ci.org/deardurham/dear-petition.svg?branch=master)](https://travis-ci.org/deardurham/dear-petition)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

- [DEAR Petition](#dear-petition)
  - [🚀 Docker Quick Start (recommended)](#-docker-quick-start-recommended)
  - [Frontend Development](#frontend-development)
    - [🚀 Quick Setup](#-quick-setup)
    - [API Proxy Configuration](#api-proxy-configuration)
      - [Docker Container](#docker-container)
      - [Local Frontend](#local-frontend)
  - [Backend Development (with Docker)](#backend-development-with-docker)
    - [Using docker-compose.override.yml](#using-docker-composeoverrideyml)
    - [Initial Setup](#initial-setup)
    - [Restore database](#restore-database)
  - [Backend Development (without Docker)](#backend-development-without-docker)
    - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
    - [Setting Up Your Users](#setting-up-your-users)
  - [Development Tools and Testing](#development-tools-and-testing)
    - [Type checks](#type-checks)
    - [Test coverage](#test-coverage)
    - [Running tests with py.test](#running-tests-with-pytest)
      - [Docker](#docker)
      - [Without Docker](#without-docker)
    - [Sign up for Sentry](#sign-up-for-sentry)
- [Production testing](#production-testing)

## 🚀 Docker Quick Start (recommended)

```bash
git clone git@github.com:deardurham/dear-petition.git
cd dear-petition
docker-compose up -d django
docker-compose run --rm django python manage.py createsuperuser
```


## Frontend Development

The user facing side of the DEAR Petition Generator is a React single page app (SPA). It is common to run the frontend locally while running the backend on docker.


### 🚀 Quick Setup

```bash
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

#### Local Frontend

When using `npm run start` to run the frontend, the `API_PROXY` environment variable is unset. The fallback proxy is set to the `http://localhost:8000`.

You can set the proxy url by either setting `OVERRIDE_API_PROXY` or `API_PROXY`:

```bash
API_PROXY=http://localhost:8888 npm start
```

## Backend Development (with Docker)

To run this on a Mac, use [Docker for
Mac](https://docs.docker.com/docker-for-mac/install/).

Build the project containers:

    docker-compose build

Run the containers:

    docker-compose up django

Visit http://localhost:8000/petition/api/ in your browser.

### Using docker-compose.override.yml

To develop in a Docker container, we'll use a `docker-compose.override.yml`
override file to configure the Django container to sleep by default:

```yaml
# file: docker-compose.override.yml
version: '3'

services:
  django:
    command: ["sleep", "infinity"]
```

Now we run `runserver` manually to have more control over restarts:

```sh
docker compose exec django bash
root$ python manage.py runserver 0.0.0.0:8000
```

### Initial Setup

Create a superuser:

    docker-compose run --rm django python manage.py createsuperuser

Migrate DB:

    docker-compose run --rm django python manage.py migrate

See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


### Restore database

To restore a database dump, you can run:

```sh
docker-compose run --rm django sh
$ dropdb dear_petition
$ createdb dear_petition
$ pg_restore -Ox -d dear_petition latest.dump
$ python manage.py migrate
```


## Backend Development (without Docker)

Run the setup\_project.py script from the base directory, providing as a
command line argument the directory to the related ciprs-reader project.
This will set up the project in your environment.


### Setting Up a Virtual Environment

Developing inside a virtual environment is recommended.

On Mac run the following command to set up a virtual environment:
```
brew install pipenv
pipenv shell
pip install -r requirements/base.txt
```

On Linux run the following command to set up a virtual environment:
```
sudo yum install python-tools
pip3 install pipenv
pipenv shell
pip install -r requirements/base.txt
```

While inside of the pipenv run the setup\_project.py script from the base directory, providing as a
command line argument the directory to the related ciprs-reader project.
This will set up the project in your environment.
```
python3 setup-project.py <path-to-ciprs-reader>
```

Additional Pipenv Notes:
To exit the pip environment:
```
(dear-petition) bash-3.2$ exit
exit
bash-3.2$
```

To delete the pipenv environment:
```
bash-3.2$ pipenv --rm
Removing virtualenv (/Users/user/.local/share/virtualenvs/dear-petition-fJpn7FEC)…
```


### Setting Up Your Users

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

## Development Tools and Testing

### Running tests with py.test

#### Docker

    $ docker-compose run --rm django pytest

#### Without Docker

    $ pytest
    
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
