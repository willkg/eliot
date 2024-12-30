FROM --platform=linux/amd64 python:3.11.11-slim-bullseye@sha256:9d6c8e7c36da7e7a77af6b503877fe0dece3aa239be502ecb62f3ac266ce6011

ARG groupid=5000
ARG userid=5000

WORKDIR /app/

RUN groupadd -r kent && useradd --no-log-init -r -g kent kent

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install -U 'pip>=20' && \
    pip install --no-cache-dir 'kent==2.0.0'

USER kent

ENTRYPOINT ["/usr/local/bin/kent-server"]
CMD ["run"]
