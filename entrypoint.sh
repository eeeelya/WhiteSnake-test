#!/bin/sh

python car_shop/manage.py makemigrations
python car_shop/manage.py migrate
python car_shop/manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python car_shop/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python car_shop/manage.py runserver 0.0.0.0:8000

exec "$@"