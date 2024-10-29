# NOTE(smarnach): To upgrade Python to a new minor or major version, see
# https://mozilla-eliot.readthedocs.io/en/latest/dev.html#how-to-upgrade-the-python-version
FROM --platform=linux/amd64 python:3.11.10-slim-bullseye@sha256:f6a64ef0a5cc14855b15548056a8fc77f4c3526b79883fa6709a8e23f676ac34

ARG userid=10001
ARG groupid=10001

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/ \
    PORT=8000

EXPOSE $PORT

WORKDIR /app

# add a non-privileged user for installing and running the application
RUN groupadd --gid $groupid app && \
    useradd -g app --uid $userid --shell /usr/sbin/nologin --create-home app && \
    chown app:app /app/

# install a few essentials and clean apt caches afterwards
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-transport-https build-essential curl git libpq-dev gettext libffi-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
COPY requirements.txt /tmp/

# Switch to /tmp to install dependencies outside home dir
WORKDIR /tmp

RUN pip install -U 'pip>=20' && \
    pip install --no-cache-dir --no-deps -r requirements.txt && \
    pip check --disable-pip-version-check

COPY . /app

# Switch back to home directory
WORKDIR /app

RUN chown -R app:app /app

USER app

ENTRYPOINT ["/bin/bash", "/app/bin/entrypoint.sh"]

CMD ["eliot"]
