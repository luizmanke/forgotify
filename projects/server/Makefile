include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-unit

shell: docker-shell

server:
	${DOCKER_RUN} \
		-e MEDIA_PROVIDER_CLIENT_ID \
		-e MEDIA_PROVIDER_CLIENT_SECRET \
		-p 80:80 \
			${PROJECT_NAME} uvicorn server.main:app --host 0.0.0.0 --port 80

clean: docker-images-remove

.PHONY: server
