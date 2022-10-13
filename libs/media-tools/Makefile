PROJECT_NAME := media-tools

PWD := $(shell pwd)

TEST_FOLDER := tests
TEST_VOLUME := -v ${PWD}/${TEST_FOLDER}:/app/${TEST_FOLDER}
TEST_CMD := pytest -v

DOCKER_RUN := docker run --rm


all: build lint tests

build:
	docker build -t ${PROJECT_NAME} .

flake8:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} flake8 --max-line-length 120

mypy:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} mypy . --ignore-missing-imports

bandit:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} bandit .

lint: flake8 mypy bandit

check:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} ${TEST_CMD} ${TEST_FOLDER}/unit

shell:
	${DOCKER_RUN} -it ${PROJECT_NAME} python

tests: check
