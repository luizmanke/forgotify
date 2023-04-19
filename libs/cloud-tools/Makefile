include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-integration-wait docker-compose-stop

shell: docker-compose-shell-wait docker-compose-stop

stop: docker-compose-stop

clean: docker-containers-stop docker-containers-remove docker-images-remove
