include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk
include ../../makefiles/Registry.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-unit

shell: docker-shell

push: registry-create registry-push

clean: docker-images-remove
