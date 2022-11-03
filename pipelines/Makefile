include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Test.mk


all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

clean: docker-images-remove
