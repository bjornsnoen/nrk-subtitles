from python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt
COPY docker-stuff/install-deps.sh /app/docker-stuff/install-deps.sh

WORKDIR /app

RUN sh docker-stuff/install-deps.sh

COPY . /app

RUN sh docker-stuff/cleanup.sh

COPY docker-stuff/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker-stuff/nginx.conf /etc/nginx/sites-enabled/subs.conf

CMD [ "/usr/bin/supervisord" ]