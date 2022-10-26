PROJECT_DIR := $(shell pwd)

DOCKER_RUN := docker run --rm

DOCKER_COMPOSE_RUN := docker-compose run --rm


guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set!"; \
		exit 1; \
	fi

alembic-apply:
	${DOCKER_COMPOSE_RUN} migrations sh -c "/wait && alembic upgrade heads"

alembic-revision: guard-MSG
	${DOCKER_COMPOSE_RUN} migrations sh -c "/wait && alembic upgrade heads && alembic revision --autogenerate -m '${MSG}'"

alembic-apply-remote: guard-POSTGRES_HOST guard-POSTGRES_PORT guard-POSTGRES_USERNAME guard-POSTGRES_PASSWORD guard-POSTGRES_DATABASE
	${DOCKER_RUN} \
		-e POSTGRES_HOST \
		-e POSTGRES_PORT \
		-e POSTGRES_USERNAME \
		-e POSTGRES_PASSWORD \
		-e POSTGRES_DATABASE \
		-v ${PROJECT_DIR}/alembic.ini:/app/alembic.ini \
		-v ${PROJECT_DIR}/migrations/:/app/migrations/ \
			batch-database-update:latest sh -c "alembic upgrade heads"
