MAKEFILE_DIR := $(lastword ${MAKEFILE_LIST})
REPO_DIR := $(shell echo ${MAKEFILE_DIR} | sed 's#/makefiles.*##')

PROJECT_DIR := $(shell pwd)
PROJECT_NAME := $(shell basename ${PROJECT_DIR})

REGISTRY_IMAGE := registry
REGISTRY_URI := ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

TAG := $(shell git rev-parse --short HEAD)
PROJECT_AWS_IMAGE := ${REGISTRY_URI}/${PROJECT_NAME}:${TAG}

DOCKER_RUN := docker run --rm

SUPPRESS_OUTPUT := > /dev/null 2>&1


guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set!"; \
		exit 1; \
	fi

registry-build:
	docker build \
		-t ${REGISTRY_IMAGE} \
		-f ${REPO_DIR}/dockerfiles/Dockerfile.aws \
		.

registry-create: registry-build guard-AWS_ACCESS_KEY_ID guard-AWS_SECRET_ACCESS_KEY guard-AWS_REGION
	${DOCKER_RUN} \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_REGION \
			${REGISTRY_IMAGE} \
				aws ecr create-repository --repository-name ${PROJECT_NAME} ${SUPPRESS_OUTPUT}; \
				echo Registry ${PROJECT_NAME} created.

registry-tag: guard-AWS_ACCOUNT_ID guard-AWS_REGION
	docker tag ${PROJECT_NAME} ${PROJECT_AWS_IMAGE}

registry-push: registry-build registry-tag guard-AWS_ACCOUNT_ID guard-AWS_ACCESS_KEY_ID guard-AWS_SECRET_ACCESS_KEY guard-AWS_REGION
	${DOCKER_RUN} \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_REGION \
		-v /var/run/docker.sock:/var/run/docker.sock \
			${REGISTRY_IMAGE} \
				aws ecr get-login-password | docker login --username AWS --password-stdin ${REGISTRY_URI} && \
				docker push ${PROJECT_AWS_IMAGE}
