#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# default variables
: "${PORT:=8000}"
: "${ELIOT_GUNICORN_WORKERS:=1}"
: "${ELIOT_GUNICORN_TIMEOUT:=300}"
: "${ELIOT_GUNICORN_MAX_REQUESTS:=0}"
: "${ELIOT_GUNICORN_MAX_REQUESTS_JITTER:=0}"

(set -o posix; set) | grep ELIOT_GUNICORN

cd /app/

gunicorn \
    --bind 0.0.0.0:"${PORT}" \
    --timeout "${ELIOT_GUNICORN_TIMEOUT}" \
    --workers "${ELIOT_GUNICORN_WORKERS}" \
    --max-requests="${ELIOT_GUNICORN_MAX_REQUESTS}" \
    --max-requests-jitter="${ELIOT_GUNICORN_MAX_REQUESTS_JITTER}" \
    --access-logfile - \
    eliot.wsgi:application
