include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk
include ../../makefiles/Registry.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-integration-wait stop

shell: docker-shell

stop: docker-compose-stop

push: registry-create registry-push

clean: docker-images-remove
