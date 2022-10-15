include ../../tools/Docker.mk
include ../../tools/Lint.mk
include ../../tools/Poetry.mk
include ../../tools/Test.mk


all: build lint test

lock: poetry-lock

build: lock docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: test-integration

shell: docker-compose-shell

stop: docker-compose-stop

clean: docker-containers-stop docker-containers-remove docker-images-remove
