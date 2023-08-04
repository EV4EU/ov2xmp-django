# pull official base image
FROM python:3.10-slim

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt .

RUN apt update \
    && apt install -y gcc libldap2-dev libsasl2-dev ldap-utils python3-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy source code to /code/
COPY . .

EXPOSE 8000
EXPOSE 9000

RUN chmod +x entrypoint.sh

# run entrypoint.prod.sh
CMD ["/code/entrypoint.sh"]

# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
