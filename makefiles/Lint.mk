PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})
PROJECT_FOLDER := $(subst -,_,${PROJECT_NAME})

TEST_FOLDER := tests
TEST_VOLUME := -v ${PROJECT_DIR}/${TEST_FOLDER}:/app/${TEST_FOLDER}

DOCKER_WORKDIR := --workdir /app
DOCKER_RUN := docker run --rm


lint-flake8:
	${DOCKER_RUN} ${DOCKER_WORKDIR} ${TEST_VOLUME} --entrypoint flake8 ${PROJECT_NAME} ${PROJECT_FOLDER} ${TEST_FOLDER} --max-line-length 120

lint-mypy:
	${DOCKER_RUN} ${DOCKER_WORKDIR} ${TEST_VOLUME} --entrypoint mypy ${PROJECT_NAME} ${PROJECT_FOLDER} ${TEST_FOLDER} --ignore-missing-imports

lint-bandit:
	${DOCKER_RUN} ${DOCKER_WORKDIR} ${TEST_VOLUME} --entrypoint bandit ${PROJECT_NAME} .
