#!/bin/bash
if [[ ! -f /mapproxy/uwsgi.ini ]]; then
    echo "uwsgi.ini was not found creating from uwsgi.default.ini"
    envsubst '${PROCESSES} ${THREADS}' < /mapproxy/uwsgi.default.ini > /mapproxy/settings/uwsgi.ini
else
    cp -f /mapproxy/uwsgi.ini /mapproxy/settings/uwsgi.ini
fi

if [[ ! -f /mapproxy/log.yaml ]]; then
    echo "log.yaml was not found creating from log.default.yaml"
    envsubst '${LOG_LEVEL} ${REQUESTS_LOG_LEVEL}' < /mapproxy/log.default.yaml > /mapproxy/settings/log.yaml
else
    cp -f /mapproxy/log.yaml /mapproxy/settings/log.yaml
fi

sed -i -e "s/uid = 1000/uid = $(id -u)/g" /mapproxy/settings/uwsgi.ini
exec /usr/local/bin/uwsgi --ini /mapproxy/settings/uwsgi.ini
