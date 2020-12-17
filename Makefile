.DEFAULT_GOAL := run

.PHONY: docker-images run

registry = registry.digitalocean.com

prod:
	docker build . -f docker/fastapi/Dockerfile --target=runner -t $(registry)/brbcoffee/site:subs

push: prod
	docker push $(registry)/brbcoffee/site:subs

run: prod
	docker-compose up -d