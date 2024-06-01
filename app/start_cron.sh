#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment
echo "0 0 */1 * * /usr/local/bin/python /app/app/manage.py popularity_step >> /popularity_cron.log 2>&1" |  crontab -
service cron start