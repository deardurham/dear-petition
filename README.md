# DEAR Petition

A [Durham Expunction and Restoration (DEAR)](https://www.deardurham.org)
project for creating petition forms.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)](https://github.com/pydanny/cookiecutter-django/)
[![Build Status](https://travis-ci.org/deardurham/dear-petition.svg?branch=master)](https://travis-ci.org/deardurham/dear-petition)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Frontend Development
See [frontend README](frontend/README.md) for steps

## Local Development

Begin by cloning the repository:

```
git clone git@github.com:deardurham/dear-petition.git
```


## Local Development with Docker

To run this on a Mac, use [Docker for
Mac](https://docs.docker.com/docker-for-mac/install/).

Add desired environment variables to the `.env` file before creating your virtual environment.  You can copy `.env.example` to get started. Create a `.env` file with the following:

    COMPOSE_FILE=local.yml

Build the project containers:

    docker-compose build

Run the containers:

    docker-compose up -d

Visit http://localhost:8000 in your browser.


### Initial Setup

Create a superuser:

    docker-compose run --rm django python manage.py createsuperuser

Migrate DB:

    docker-compose run --rm django python manage.py migrate

See detailed [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).


## Setup (without Docker)

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


Settings
--------

Moved to
[settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Basic Commands
--------------

#### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out
    the form. Once you submit it, you\'ll see a \"Verify Your E-mail
    Address\" page. Go to your console to see a simulated email
    verification message. Copy the link into your browser. Now the
    user\'s email should be verified and ready to go.
-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

#### Type checks

Running type checks with mypy:

    $ mypy dear_petition

#### Test coverage

To run the tests, check your test coverage, and generate an HTML
coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

### Running tests with py.test

    $ pytest

#### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS
compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

#### Celery

This app comes with Celery.

To run a celery worker:

``` {.sourceCode .bash}
cd dear_petition
celery -A dear_petition.taskapp worker -l info
```

Please note: For Celery\'s import magic to work, it is important *where*
the celery commands are run. If you are in the same folder with
*manage.py*, you should be right.

#### Email Server

In development, it is often nice to be able to see emails that are being
sent from your application. For that reason local SMTP server
[MailHog](https://github.com/mailhog/MailHog) with a web interface is
available as docker container.

Container mailhog will start automatically when you will run all docker
containers. Please check [cookiecutter-django Docker
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html)
for more details how to start all containers.

With MailHog running, to view messages that are sent by your
application, open your browser and go to `http://127.0.0.1:8025`

#### Sentry

Sentry is an error logging aggregator service. You can sign up for a
free account at <https://sentry.io/signup/?code=cookiecutter> or
download and host it yourself. The system is setup with reasonable
defaults, including 404 logging and integration with the WSGI
application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

#### Heroku

See detailed [cookiecutter-django Heroku
documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).
