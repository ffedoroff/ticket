#!/usr/bin/env sh

set -o errexit
set -o nounset

uwsgi \
  --socket 0.0.0.0:5004 \
  --harakiri 600 \
  --protocol uwsgi \
  --static-map /static=/var/www/django/static \
  --threads 5 \
  --idle \
  --die-on-idle \
  --cheap \
  --disable-logging \
  --wsgi-file /code/server/wsgi.py
