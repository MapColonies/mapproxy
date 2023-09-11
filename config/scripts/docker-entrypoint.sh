#!/bin/bash
if [[ ! -f /mapproxy/uwsgi.ini ]]; then
    echo "uwsgi.ini was not found creating from uwsgi.default.ini"
    envsubst '${PROCESSES} ${THREADS}' < /mapproxy/uwsgi.default.ini > /mapproxy/uwsgi.ini
fi

if [[ ! -f /mapproxy/log.yaml ]]; then
    echo "log.yaml was not found creating from log.default.yaml"
    envsubst '${LOG_LEVEL} ${REQUESTS_LOG_LEVEL}' < /mapproxy/log.default.yaml > /mapproxy/log.yaml
fi

exec /usr/local/bin/uwsgi --ini /mapproxy/uwsgi.ini
