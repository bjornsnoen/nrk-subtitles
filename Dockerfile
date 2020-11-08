from python:3.8-slim-buster

COPY requirements.txt /app/requirements.txt
COPY src/docker-stuff/install-deps.sh /app/docker-stuff/install-deps.sh

WORKDIR /app

RUN sh docker-stuff/install-deps.sh

COPY src /app

RUN sh docker-stuff/cleanup.sh

COPY src/docker-stuff/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY src/docker-stuff/nginx.conf /etc/nginx/sites-enabled/subs.conf

CMD [ "/usr/bin/supervisord" ]