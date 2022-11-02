include ../../makefiles/Alembic.mk
include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Poetry.mk
include ../../makefiles/Test.mk


all: build lint test

lock: poetry-lock

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

migrations-apply-remote: alembic-apply-remote

migrations-revision: alembic-revision docker-compose-stop

test: alembic-apply test-integration docker-compose-stop

shell: alembic-apply docker-compose-shell docker-compose-stop

stop: docker-compose-stop

clean: docker-containers-stop docker-containers-remove docker-images-remove
