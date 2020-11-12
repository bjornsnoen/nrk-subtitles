from python:3.8-slim-buster

# Must be built from project root

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY docker/flask/install-deps.sh /app/docker/flask/install-deps.sh

WORKDIR /app

RUN sh docker/flask/install-deps.sh

COPY skam /app/skam
COPY docker/flask /app/docker/flask

RUN sh docker/flask/cleanup.sh

COPY docker/flask/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/flask/nginx.conf /etc/nginx/sites-enabled/subs.conf

# So we can create cache files from the webapp
RUN chown -R www-data:www-data /app

CMD [ "/usr/bin/supervisord" ]