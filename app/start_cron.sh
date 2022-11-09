#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment
#echo "0 12 */1 * * /usr/local/bin/python /app/app/manage.py popularity_step >> /app/app/popularity_cron.log 2>&1" |  crontab -
echo "* * * * * /usr/local/bin/python /app/app/manage.py popularity_step >> /popularity_cron.log 2>&1" |  crontab -
#echo "* * * * * printenv >> /popularity_cron.log 2>&1" |  crontab -
service cron start