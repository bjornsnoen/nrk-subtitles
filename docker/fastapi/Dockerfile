# Must be built from project root
ARG image_type=without_debug

FROM python:3.8-slim-buster as debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.debug.conf /etc/supervisor/conf.d/supervisor.conf
ENV DEBUG=1
ENV DEBUG_LISTEN_HOST="0.0.0.0"
ENV DEBUG_LISTEN_PORT=5678

FROM python:3.8-slim-buster as without_debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisor.conf


FROM ${image_type}

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY docker/fastapi/install-deps.sh /app/docker/fastapi/install-deps.sh

WORKDIR /app

RUN sh docker/fastapi/install-deps.sh

COPY skam /app/skam
COPY docker/fastapi /app/docker/fastapi

RUN sh docker/fastapi/cleanup.sh

COPY docker/fastapi/supervisor/${supervisorconf} /etc/supervisor/conf.d/supervisord.conf
COPY docker/fastapi/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/fastapi/nginx/application.conf /etc/nginx/sites-enabled/application.conf

# So we can create cache files from the webapp
RUN chown -R www-data:www-data /app

CMD [ "/usr/bin/supervisord" ]