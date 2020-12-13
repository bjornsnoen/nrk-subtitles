# Must be built from project root
ARG image_type=without_debug

FROM python:3.8-alpine as backend-builder
COPY docker/fastapi/install-deps.sh /app/docker/fastapi/install-deps.sh
RUN sh /app/docker/fastapi/install-deps.sh

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
COPY frontend/package.json frontend/yarn.lock /app/frontend/
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install

COPY subtitles /app/subtitles
COPY frontend/src /app/frontend/src
COPY frontend/public/ /app/frontend/public
COPY frontend/tsconfig.json /app/frontend/

COPY docker/fastapi/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/fastapi/nginx/application.conf /etc/nginx/conf.d/application.conf


FROM node:alpine as frontend-builder
COPY --from=backend-builder /app/frontend /app/frontend
WORKDIR /app/frontend
RUN yarn install --dev && yarn build


FROM python:3.8-alpine as debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.debug.conf /etc/supervisor.d/app.ini
ENV DEBUG=1 \
 DEBUG_LISTEN_HOST="0.0.0.0" \
 DEBUG_LISTEN_PORT=5678

FROM python:3.8-alpine as without_debug
ONBUILD COPY docker/fastapi/supervisor/supervisord.conf /etc/supervisor.d/app.ini
ONBUILD COPY docker/fastapi/gunicorn.config.py /gunicorn.config.py


FROM ${image_type} as runner
RUN apk add supervisor sqlite nginx-mod-http-lua lua-resty-core nginx
COPY --from=backend-builder --chown=nobody /app /app
COPY --from=backend-builder /etc/nginx /etc/nginx
COPY --from=frontend-builder /app/frontend/build /app/frontend/build
ENV API_ROOT_PATH="/api"
CMD [ "/usr/bin/supervisord" ]
