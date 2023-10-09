# TeleBand

The music education learning management system

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands


### Setting Up Postgres

-   Download Postgres for your operating system and keep note of the username and password you create in the installation process

### Install all Requirements

        $ pip install -r requirements/local.txt


### Create .env File in Project Root

-   Create file called .env in project root with the line 

        DATABASE_URL=postgres://user:pass@localhost/teleband

    Where user and pass are the username and password of the postgres user you created


### Create Postgres Database

-   Create a Postgres Database with your created user


### Run Migrate

        $ python manage.py migrate


### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

- To create a Teacher:
        1. use the admin pages
        1. create a user
        1. edit that user and select an instrument for them
        1. add them to the Teacher group

### Type checks

Running type checks with mypy:

    $ mypy teleband

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use [MailHog](https://github.com/mailhog/MailHog) when generating the project a local SMTP server with a web interface will be available.

1.  [Download the latest MailHog release](https://github.com/mailhog/MailHog/releases) for your OS.

2.  Rename the build to `MailHog`.

3.  Copy the file to the project root.

4.  Make it executable:

        $ chmod +x MailHog

5.  Spin up another terminal window and start it there:

        ./MailHog

6.  Check out <http://127.0.0.1:8025/> to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

## Deployment

The following details how to deploy this application.
1. tag the version `git tag <whatever, e.g. v0.2.2>`
1. push the tag `git push origin <whatever, e.g. v0.2.2>`
1. on the server, get to the main repo root e.g. `cd ~/MusicCPRDev`
1. pull on server `git pull`
1. checkout a new worktree for the recently pushed/fetched/tagged version `git worktree add ../dev-versions/v0.2.2 v0.2.2`
1. cd ~/dev-versions/v0.2.2/ 
1. cp ../<prev-version>/.env* .
<!-- 1. mkdir logs -->
1. source ~/venv-dev/bin/activate
<!-- 1. pip install -r requirements/production.txt # maybe don't need this because no new requirements? -->
1. stop old version `sudo supervisorctl stop dev_api_musiccpr`
1. migrate `python manage.py migrate`
1. change symlink `cd ~/dev-versions; rm live; ln -s /home/ec2-user/dev-versions/v0.2.2 live`
1. sudo supervisorctl start dev_api_musiccpr

# Renewing SSL Certs (requires creating DNS TXT Entries rn 😕)
1. maybe this is the command? 
    * `sudo certbot certonly --manual --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges dns-01 -d "*.musiccpr.org,musiccpr.org"`
# Deploying to Prod first time
Prefer to have:
1. same ec2 instance as dev
1. a different RDS instance (for postgres database)
1. a different s3 bucket (or path?)

## Creating RDS Instance
1. use web console. choose postgres, accept defaults, but choose free tier, choose some sort of connectivity thing that goes to the ec2 instance, choose existing security group(s) ("default")
1. create a user for the app
        1. connect to new db via psql like `psql postgres://...`
        1. create user with `CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';`
1. create database `CREATE DATABASE yourdbname;`
1. give user privileges `GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;`
1. copy dev's .env and make new (prod) values.
        * where to get aws access stuff?
                1. create IAM user
                        * permissions policies: `AnyMailSESRecommended`
                        * go to security credentials tab and `create access key`
1. create s3 bucket, copy settings from existing bucket
1. activate venv
1. pip install -r requirements/production.txt
1. python manage.py migrate
1. copy (and update) nginx fe and be configs from dev for prod
1. copy (and update) supervisor config from dev for prod see: `/etc/supervisorctl
1. sudo supervisorctl reread

## Media (sample audio) Files not working in deployed environment
1. i needed to tell s3 bucket that it should make another directory public access

