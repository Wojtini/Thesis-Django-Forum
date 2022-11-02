#!/bin/sh

cd app || exit
rm /app/staticfiles -r
python manage.py collectstatic
#python manage.py compress --force

./start_cron.sh

gunicorn --bind 0.0.0.0:8000 --workers=6 Masquerade.wsgi &
P1=$!
daphne -b 0.0.0.0 -p 8010 Masquerade.asgi:application &
P2=$!
wait $P1 $P2