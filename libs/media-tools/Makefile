include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Poetry.mk
include ../../makefiles/Test.mk


all: build lint test

lock: poetry-lock

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

shell: docker-shell

clean: docker-images-remove
