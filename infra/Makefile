include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Test.mk

FLAGS := 
STACK := dev


all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

test: test-unit

shell: docker-shell

up:
	pulumi update --stack ${STACK} ${FLAGS}

list-stacks:
	pulumi stack ls

clean: docker-images-remove
