PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})

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

alembic-apply-remote: guard-DATABASE_HOST guard-DATABASE_PORT guard-DATABASE_USERNAME guard-DATABASE_PASSWORD guard-DATABASE_NAME
	${DOCKER_RUN} \
		-e DATABASE_HOST \
		-e DATABASE_PORT \
		-e DATABASE_USERNAME \
		-e DATABASE_PASSWORD \
		-e DATABASE_NAME \
		-v ${PROJECT_DIR}/alembic.ini:/app/alembic.ini \
		-v ${PROJECT_DIR}/migrations/:/app/migrations/ \
			${PROJECT_NAME} sh -c "alembic upgrade heads"
