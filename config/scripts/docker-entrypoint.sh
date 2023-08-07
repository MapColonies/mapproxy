#!/bin/bash
# substitute env var values
envsubst '${PROCESSES} ${THREADS}' < /mapproxy/uwsgi.default.conf > /mapproxy/uwsgi.conf
envsubst < /mapproxy/log.default.yaml > /mapproxy/log.yaml

# check if the mode variable is provided
if [ -z "$1" ]; then
  echo "Please provide a mapproxy mode variable."
  exit 1
fi

# call start.sh, of the official mapproxy distribution, uses a variable to select a mode to start mapproxy
source ./start.sh "$1"