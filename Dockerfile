# pull official base image
FROM python:3.10-slim

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ../requirements.txt .

RUN apk update --no-cache \
    && apk add --virtual build-deps gcc python3-dev musl-dev build-base \
    && apk add libpq postgresql-dev openssl-dev cargo jpeg-dev zlib-dev libffi-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt  \
    && apk del build-deps

# Copy source code to /code/
COPY . .
#COPY ../nginx/tls/sdn_dashboard.crt /etc/nginx/tls/sdn_dashboard.crt
#COPY ../nginx/tls/sdn_dashboard.key /etc/nginx/tls/sdn_dashboard.key

EXPOSE 8000

RUN chmod +x entrypoint.sh

# run entrypoint.prod.sh
CMD ["/code/entrypoint.sh"]

# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
