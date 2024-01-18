#!/bin/bash

if [[ ! -f /mapproxy/log.yaml ]]; then
    echo "log.yaml was not found creating from log.default.yaml"
    envsubst '${LOG_LEVEL} ${REQUESTS_LOG_LEVEL}' < /mapproxy/log.default.yaml > /mapproxy/settings/log.yaml
else
    cp -f /mapproxy/log.yaml /mapproxy/settings/log.yaml
fi

exec gunicorn
