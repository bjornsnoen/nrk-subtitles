# Must be built from project root
ARG image_type=without_debug

FROM python:3.8-slim-buster as build-deps
COPY docker/fastapi/install-deps.sh /app/docker/fastapi/install-deps.sh
RUN sh /app/docker/fastapi/install-deps.sh
COPY docker/fastapi/cleanup.sh docker/fastapi/cleanup.sh
RUN sh docker/fastapi/cleanup.sh


FROM build-deps as debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.debug.conf /etc/supervisor/conf.d/supervisor.conf
ENV DEBUG=1 \
 DEBUG_LISTEN_HOST="0.0.0.0" \
 DEBUG_LISTEN_PORT=5678


FROM build-deps as without_debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisor.conf


FROM ${image_type}

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
COPY frontend/package.json frontend/yarn.lock /app/frontend/
RUN chown -R www-data:www-data /app /var/www /app

USER www-data
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install
RUN cd frontend && yarn install --dev

COPY --chown=www-data:www-data subtitles /app/subtitles
COPY --chown=www-data:www-data docker/fastapi /app/docker/fastapi
COPY --chown=www-data:www-data frontend/src /app/frontend/src
COPY --chown=www-data:www-data frontend/public/ /app/frontend/public
COPY --chown=www-data:www-data frontend/tsconfig.json /app/frontend/

WORKDIR /app/frontend
RUN yarn build
WORKDIR /app

COPY docker/fastapi/nginx/nginx.conf /etc/nginx/nginx.conf
ENV API_ROOT_PATH="/api"
COPY docker/fastapi/nginx/application.conf /etc/nginx/sites-enabled/application.conf

USER root
CMD [ "/usr/bin/supervisord" ]