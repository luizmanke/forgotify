include ../../tools/Docker.mk
include ../../tools/Lint.mk
include ../../tools/Poetry.mk
include ../../tools/Test.mk


all: build lint test

lock: poetry-lock

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

shell: docker-shell

clean: docker-images-remove
