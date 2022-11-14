include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Test.mk


all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

shell: docker-shell

server:
	${DOCKER_RUN} \
		-e MEDIA_PROVIDER_CLIENT_ID \
		-e MEDIA_PROVIDER_CLIENT_SECRET \
		-e DATABASE_HOST \
		-e DATABASE_PORT \
		-e DATABASE_USERNAME \
		-e DATABASE_PASSWORD \
		-e DATABASE_NAME \
		-p 3000:3000 \
			${PROJECT_NAME} dagit -h 0.0.0.0

clean: docker-images-remove
