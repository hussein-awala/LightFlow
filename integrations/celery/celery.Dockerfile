FROM python:3.11-slim

ARG CELERY_VERSION=5.3.4

RUN pip install celery[amqp,redis]==$CELERY_VERSION flower==2.0.1
