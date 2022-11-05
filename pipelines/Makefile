include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Test.mk


all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

server:
	${DOCKER_RUN} \
		-e MEDIA_TOOLS_CLIENT_ID \
		-e MEDIA_TOOLS_CLIENT_SECRET \
		-e POSTGRES_HOST \
		-e POSTGRES_PORT \
		-e POSTGRES_USERNAME \
		-e POSTGRES_PASSWORD \
		-e POSTGRES_DATABASE \
		-p 3000:3000 \
			${PROJECT_NAME} dagit -h 0.0.0.0

clean: docker-images-remove
