# DEAR Petition

A [Durham Expunction and Restoration (DEAR)](https://www.deardurham.org)
project for creating petition forms.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Build Status](https://travis-ci.org/deardurham/dear-petition.svg?branch=master)](https://travis-ci.org/deardurham/dear-petition)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Local Development

Begin by cloning the repository:

```
git clone git@github.com:deardurham/dear-petition.git
```


## Frontend Development

The user facing side of the DEAR Petition Generator is a React single page app (SPA).


### 🚀 Quick Setup

```bash
npm i
npm run start
```


### Staging Backend

By default, the frontend development server [proxies requests](https://create-react-app.dev/docs/proxying-api-requests-in-development/) to [a staging API server](https://dear-petition-staging.herokuapp.com/).

The staging API server is useful for developers who do not wish to build a local backend implementation. New developers must have a user set up on the staging server in order to test most frontend functionality.


### Local Backend

Developers who wish to use a local version of both the frontend and backend must set the `proxy` variable in `package.json` to the following:

```diff
-  "proxy": "https://dear-petition-staging.herokuapp.com/",
+  "proxy": "http://localhost:8000",
```


## Backend Development (with Docker)

To run this on a Mac, use [Docker for
Mac](https://docs.docker.com/docker-for-mac/install/).

Build the project containers:

    docker-compose build

Run the containers:

    docker-compose up -d django

Visit http://localhost:8000/petition/api/ in your browser.


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


### Type checks

Running type checks with mypy:

    $ mypy dear_petition


### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

### Running tests with py.test

    $ pytest
