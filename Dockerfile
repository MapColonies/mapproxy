# syntax=docker/dockerfile:1
ARG TARGET_BUILD=nginx
FROM ghcr.io/mapproxy/mapproxy/mapproxy:1.16.0-${TARGET_BUILD}
ARG TARGET_BUILD

ENV \
    TARGET_BUILD=${TARGET_BUILD} \
    # Keeps Python from buffering stdout and stderr to avoid situations where
    # the application crashes without emitting any logs due to buffering.
    PYTHONUNBUFFERED=1 \
    # global
    LOG_LEVEL=WARNING \
    # uwsgi
    PROCESSES=6 \
    THREADS=10 \
    # Telemetry
    TELEMETRY_TRACING_ENABLED='true' \
    TELEMETRY_ENDPOINT='localhost:4317' \
    OTEL_RESOURCE_ATTRIBUTES='service.name=mapcolonies,application=mapproxy' \
    OTEL_SERVICE_NAME='mapproxy' \
    TELEMETRY_SAMPLING_RATIO_DENOMINATOR=1000

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    # install mapproxy dependencies
    python -m pip install -r requirements.txt && \
    apt-get -y update && \
    apt-get install -y \
    gettext

WORKDIR /mapproxy

# Copy custom code and configurations.
COPY ./config/mapproxy ./config/scripts ./config/uwsgi ./

# Copy custom nginx config overriding base image's config.
COPY ./config/nginx/nginx.default.conf /etc/nginx/sites-enabled/default

# This dir is used by the official mapproxy image so it must be created.
RUN mkdir -p config/cache_data

# Expose the port that the application listens on.
EXPOSE 8080

# Run the application.
ENTRYPOINT ["bash", "-c", "./docker-entrypoint.sh $TARGET_BUILD"]
