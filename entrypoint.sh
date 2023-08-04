#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
      echo "Waiting for postgres..."
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations --noinput

python manage.py migrate --noinput

if [ -n "$OV2XMP_INITIALIZE_SUPERUSER" ] ; then
    python manage.py createsuperuser --no-input
fi

python manage.py collectstatic --noinput

(nohup sanic csms:app --host=0.0.0.0 --port=9000 --reload) &

(nohup celery -A ov2xmp worker -l info) &

daphne -b 0.0.0.0 -p 8000 ov2xmp.asgi:application
