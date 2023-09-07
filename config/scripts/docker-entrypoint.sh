#!/bin/bash
envsubst '${PROCESSES} ${THREADS}' < /mapproxy/uwsgi.default.conf > /mapproxy/uwsgi.mapproxy.conf
envsubst '${LOG_LEVEL}' < /mapproxy/log.default.yaml > /mapproxy/log.yaml

chown mapproxy:mapproxy /mapproxy/uwsgi.mapproxy.conf /mapproxy/log.yaml

if [ -z "$1" ]; then
  echo "Please provide a mapproxy mode variable."
  exit 1
fi

# the start script of the official mapproxy distribution, accepts a variable to select a mode to start mapproxy
source ./start.sh "$1"