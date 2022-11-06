PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})

TEST_FOLDER := tests
TEST_VOLUME := -v ${PROJECT_DIR}/${TEST_FOLDER}:/app/${TEST_FOLDER}

DOCKER_RUN := docker run --rm


lint-flake8:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} flake8 --max-line-length 120

lint-mypy:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} mypy . --ignore-missing-imports

lint-bandit:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} bandit .
