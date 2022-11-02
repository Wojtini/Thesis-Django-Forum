#!/bin/sh

echo "* * * * * /usr/local/bin/python /app/app/manage.py popularity_step >> /app/app/popularity_cron.log 2>&1" |  crontab -
service cron start