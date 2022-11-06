PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})
PROJECT_SERVICE := $(subst -,_,${PROJECT_NAME})

DOCKER_RUN := docker run --rm

DOCKER_COMPOSE_RUN := docker-compose run --rm


docker-build: CD=../../
docker-build:
	$(eval REPO_DIR := $(shell cd ${CD} && pwd))
	$(eval PROJECT_PATH := $(subst ${REPO_DIR}/,,${PROJECT_DIR}))
	cd ${REPO_DIR} && \
	docker build \
		-t ${PROJECT_NAME} \
		-f ${PROJECT_DIR}/Dockerfile \
		--build-arg PROJECT_PATH=$(PROJECT_PATH) \
		.

docker-shell:
	${DOCKER_RUN} -it ${PROJECT_NAME} python

docker-compose-shell:
	${DOCKER_COMPOSE_RUN} ${PROJECT_SERVICE} sh -c "python"

docker-compose-shell-wait:
	${DOCKER_COMPOSE_RUN} ${PROJECT_SERVICE} sh -c "/wait && python"

docker-compose-stop:
	docker-compose down --remove-orphans

docker-containers-stop:
	docker stop $(shell docker ps -a -q --filter name=${PROJECT_NAME})

docker-containers-remove:
	docker rm $(shell docker ps -a -q --filter name=${PROJECT_NAME})

docker-images-remove:
	docker rmi $(shell docker images -a -q ${PROJECT_NAME})
