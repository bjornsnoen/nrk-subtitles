.DEFAULT_GOAL := run

.PHONY: prod push run down

registry = registry.digitalocean.com

prod:
	docker build . -f docker/fastapi/Dockerfile --target=runner -t $(registry)/brbcoffee/site:subs

push: prod
	docker push $(registry)/brbcoffee/site:subs

run: prod
	docker-compose up -d

down:
	docker-compose down