FROM python:3.11.7-alpine3.19@sha256:84271da1cd297b01dd4706e01e7789b08b54a5a512c0e3fcaf11c902640f5ebd

ARG groupid=5000
ARG userid=5000

WORKDIR /app/

RUN addgroup -g $groupid app && \
    adduser --disabled-password --gecos "" --home /home/app --ingroup app --uid $userid app && \
    chown app:app /app/

RUN apk add --no-cache tini

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install -U 'pip>=20' && \
    pip install --no-cache-dir 'kent==1.0.0'

USER app

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/kent-server"]
CMD ["run"]
