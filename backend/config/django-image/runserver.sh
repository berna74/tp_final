#!/bin/bash

set -u

if [ ! -f manage.py ]
then
  django-admin startproject app .
fi

python manage.py makemigrations

until python manage.py migrate --noinput
do
  echo "Esperando a PostgreSQL para aplicar migraciones..."
  sleep 2
done

if [[ -n "$DJANGO_SU_NAME" ]]
then
  echo "from django.contrib.auth.models import User; User.objects.filter(username='${DJANGO_SU_NAME}').exists() or User.objects.create_superuser('${DJANGO_SU_NAME}', '${DJANGO_SU_EMAIL}', '${DJANGO_SU_PASSWORD}')" | python manage.py shell
fi

python manage.py runserver 0.0.0.0:8000

