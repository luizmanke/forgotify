include ../../makefiles/Docker.mk
include ../../makefiles/Lint.mk
include ../../makefiles/Pytest.mk


all: build lint test

build: docker-build

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-unit

shell: docker-shell

clean: docker-images-remove
