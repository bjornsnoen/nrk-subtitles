from python:3.8-slim-buster

# Must be built from project root

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY docker/fastapi/install-deps.sh /app/docker/fastapi/install-deps.sh

WORKDIR /app

RUN sh docker/fastapi/install-deps.sh

COPY skam /app/skam
COPY docker/fastapi /app/docker/fastapi

RUN sh docker/fastapi/cleanup.sh

COPY docker/fastapi/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/fastapi/nginx.conf /etc/nginx/sites-enabled/subs.conf

# So we can create cache files from the webapp
RUN chown -R www-data:www-data /app

CMD [ "/usr/bin/supervisord" ]