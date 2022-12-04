include ../../makefiles/Alembic.mk
include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

migrations-apply-remote: alembic-apply-remote

migrations-revision: alembic-revision docker-compose-stop

test: pytest-unit test-integration

test-integration: alembic-apply pytest-integration docker-compose-stop

test-system:
	make pytest-system OPTIONS=" \
		-e MEDIA_PROVIDER_CLIENT_ID \
		-e MEDIA_PROVIDER_CLIENT_SECRET \
		-e DATABASE_HOST \
		-e DATABASE_PORT \
		-e DATABASE_USERNAME \
		-e DATABASE_PASSWORD \
		-e DATABASE_NAME"

shell: alembic-apply docker-compose-shell docker-compose-stop

stop: docker-compose-stop

clean: docker-containers-stop docker-containers-remove docker-images-remove
