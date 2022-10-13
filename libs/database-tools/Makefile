PROJECT_NAME := database-tools
PROJECT_SERVICE := database_tools

PWD := $(shell pwd)

TEST_FOLDER := tests
TEST_VOLUME := -v ${PWD}/${TEST_FOLDER}:/app/${TEST_FOLDER}
TEST_CMD := pytest -v

DOCKER_RUN := docker run --rm
DOCKER_COMPOSE_RUN := docker-compose run --rm


all: build lint tests

build:
	docker build -t ${PROJECT_NAME} .

flake8:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} flake8 --max-line-length 120

mypy:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} mypy .

bandit:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} bandit .

lint: flake8 mypy bandit

check-integration:
	${DOCKER_COMPOSE_RUN} ${TEST_VOLUME} ${PROJECT_SERVICE} sh -c "/wait && ${TEST_CMD} ${TEST_FOLDER}/integration"

shell:
	${DOCKER_COMPOSE_RUN} database_tools sh -c "/wait && python"

stop:
	docker-compose down --remove-orphans

tests: check-integration
