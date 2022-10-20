PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})
PROJECT_SERVICE := $(subst -,_,${PROJECT_NAME})

TEST_FOLDER := tests
TEST_VOLUME := -v ${PROJECT_DIR}/${TEST_FOLDER}:/app/${TEST_FOLDER}
TEST_CMD := pytest -v

DOCKER_RUN := docker run --rm

DOCKER_COMPOSE_RUN := docker-compose run --rm


test-unit:
	${DOCKER_RUN} ${TEST_VOLUME} ${PROJECT_NAME} ${TEST_CMD} ${TEST_FOLDER}/unit

test-integration:
	${DOCKER_COMPOSE_RUN} ${TEST_VOLUME} ${PROJECT_SERVICE} sh -c "${TEST_CMD} ${TEST_FOLDER}/integration"

test-integration-wait:
	${DOCKER_COMPOSE_RUN} ${TEST_VOLUME} ${PROJECT_SERVICE} sh -c "/wait && ${TEST_CMD} ${TEST_FOLDER}/integration"
