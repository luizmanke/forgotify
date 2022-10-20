include ../../tools/Alembic.mk
include ../../tools/Docker.mk
include ../../tools/Lint.mk
include ../../tools/Poetry.mk
include ../../tools/Test.mk


all: build lint test

lock: poetry-lock

build: lock docker-build

lint: lint-flake8 lint-mypy lint-bandit

migrations-revision: alembic-revision docker-compose-stop

test: alembic-apply test-integration docker-compose-stop

shell: alembic-apply docker-compose-shell docker-compose-stop

stop: docker-compose-stop

clean: docker-containers-stop docker-containers-remove docker-images-remove
