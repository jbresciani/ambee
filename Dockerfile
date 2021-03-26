# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.8"

FROM python:${VARIANT}-slim

ENV DEBUG=True \
    SECRET_KEY=really_bad_secret_key \
    AMBEE_API_KEY=this_is_not_it

COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY requirements.txt /tmp/requirements.txt

RUN mkdir /etc/service_accounts/ \
    && pip --no-cache-dir install -U pip \
    && pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt
    
EXPOSE 8000