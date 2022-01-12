#!/bin/bash

NAME="dev_api_teleband"                                     # Name of the application
DJANGODIR=/home/deploy/dev/CPR-Music-Backend                             # Django project directory
SOCKFILE=/home/deploy/dev/CPR-Music-Backend/deploy/dev/asgi.sock # we will communicte using this unix socket
USER=deploy                                             # the user to run as
GROUP=deploy                                           # the group to run as
NUM_WORKERS=4                                           # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=config.settings.production       # which settings file should Django use
DJANGO_ASGI_MODULE=config.asgi                          # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/deploy/dev/venv/bin/activate
export DJANGO_READ_DOT_ENV_FILE=True
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_ASGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  -k uvicorn.workers.UvicornWorker \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$DJANGODIR/logs/gunicorn.log
