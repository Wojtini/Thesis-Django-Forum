#!/bin/sh

cd app || exit
rm /app/staticfiles/ -r

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py compress --force

./start_cron.sh

#uvicorn --host 0.0.0.0 --port 8000 --workers=12 Masquerade.asgi:application
gunicorn --bind 0.0.0.0:8000 --workers=12 Masquerade.wsgi