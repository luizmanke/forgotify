PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})
PROJECT_SERVICE := $(subst -,_,${PROJECT_NAME})

TEST_FOLDER := tests
TEST_VOLUME := -v ${PROJECT_DIR}/${TEST_FOLDER}:/app/${TEST_FOLDER}
TEST_CMD := pytest
TEST_VERBOSE := -v

DOCKER_WORKDIR := --workdir /app
DOCKER_RUN := docker run --rm

DOCKER_COMPOSE_RUN := docker-compose run --rm


pytest-unit:
	${DOCKER_RUN} ${DOCKER_WORKDIR} ${TEST_VOLUME} --entrypoint ${TEST_CMD} ${PROJECT_NAME} ${TEST_FOLDER}/unit ${TEST_VERBOSE}

pytest-integration:
	${DOCKER_COMPOSE_RUN} ${TEST_VOLUME} ${PROJECT_SERVICE} sh -c "${TEST_CMD} ${TEST_FOLDER}/integration ${TEST_VERBOSE}"

pytest-integration-wait:
	${DOCKER_COMPOSE_RUN} ${TEST_VOLUME} ${PROJECT_SERVICE} sh -c "/wait && ${TEST_CMD} ${TEST_FOLDER}/integration ${TEST_VERBOSE}"

pytest-system: OPTIONS=
pytest-system:
	${DOCKER_RUN} ${OPTIONS} ${TEST_VOLUME} ${PROJECT_NAME} ${TEST_CMD} ${TEST_FOLDER}/system ${TEST_VERBOSE}
