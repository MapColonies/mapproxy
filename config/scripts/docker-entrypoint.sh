#!/bin/bash
if [[ ! -f /mapproxy/uwsgi.ini ]]; then
    echo "uwsgi.ini was not found!"
else
    cp -f /mapproxy/uwsgi.ini /mapproxy/settings/uwsgi.ini
fi

if [[ ! -f /mapproxy/log.ini ]]; then
    echo "log.ini was not found!"
else
    cp -f /mapproxy/log.ini /mapproxy/settings/log.ini
fi

sed -i -e "s/uid = 1000/uid = $(id -u)/g" /mapproxy/settings/uwsgi.ini
exec /usr/local/bin/uwsgi --ini /mapproxy/settings/uwsgi.ini
