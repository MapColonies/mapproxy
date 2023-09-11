# syntax=docker/dockerfile:1
FROM ghcr.io/mapproxy/mapproxy/mapproxy:1.16.0


ENV \
    # Keeps Python from buffering stdout and stderr to avoid situations where
    # the application crashes without emitting any logs due to buffering.
    PYTHONUNBUFFERED=1 \
    # global
    LOG_LEVEL=WARNING \
    # uwsgi
    PROCESSES=6 \
    THREADS=10 \
    # Telemetry
    TELEMETRY_TRACING_ENABLED='false' \
    TELEMETRY_ENDPOINT='localhost:4317' \
    TELEMETRY_METRICS_ENABLED='false' \
    OTEL_RESOURCE_ATTRIBUTES='service.name=mapcolonies,application=mapproxy' \
    OTEL_SERVICE_NAME='mapproxy' \
    TELEMETRY_TRACING_SAMPLING_RATIO_DENOMINATOR=1000

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    # install uwsgi dependencies
    apt update && \
    apt -y install --no-install-recommends gcc && \
    # install mapproxy dependencies
    python -m pip install -r requirements.txt && \
    pip cache purge && \
    apt-get -y update && \
    apt-get install -y \
    gettext

WORKDIR /mapproxy

# Copy custom code and configurations.
COPY ./config/app ./config/scripts ./config/uwsgi ./

RUN chmod g+w ./uwsgi.default.ini ./log.default.yaml && \
    chmod -R g+w ./

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
ENTRYPOINT ["bash", "-c", "./docker-entrypoint.sh"]
