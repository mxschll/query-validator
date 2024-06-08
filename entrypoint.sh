#!/bin/bash

printf  "${CRON_SCHEDULE} cd /app/validator && /usr/local/bin/python main.py > /proc/1/fd/1 2>/proc/1/fd/2\n" > /etc/cron.d/cronjob

chmod 0644 /etc/cron.d/cronjob
/usr/bin/crontab /etc/cron.d/cronjob

printenv > /etc/environment

cron -f 
