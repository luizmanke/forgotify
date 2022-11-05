include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Test.mk


all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

server:
	${DOCKER_RUN} -p 3000:3000 ${PROJECT_NAME} dagit -h 0.0.0.0

clean: docker-images-remove
