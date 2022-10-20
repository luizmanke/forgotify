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
