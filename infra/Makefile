include ../makefiles/Docker.mk
include ../makefiles/Lint.mk
include ../makefiles/Pytest.mk

FLAGS := 
STACK := dev
AWS_IMAGE_TAG := dev


guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set!"; \
		exit 1; \
	fi

all: build lint test

build:
	make docker-build CD=../

lint: lint-flake8 lint-mypy lint-bandit

test: pytest-unit

shell: docker-shell

up: DOCKER_FLAGS=-it
up: guard-AWS_ACCOUNT_ID guard-AWS_ACCESS_KEY_ID guard-AWS_SECRET_ACCESS_KEY guard-AWS_REGION guard-PULUMI_ACCESS_TOKEN
	${DOCKER_RUN} ${DOCKER_FLAGS} \
		-e AWS_ACCOUNT_ID \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_REGION \
		-e AWS_IMAGE_TAG=${AWS_IMAGE_TAG} \
		-e PULUMI_ACCESS_TOKEN \
			${PROJECT_NAME} pulumi up --stack ${STACK} ${FLAGS}

destroy: guard-AWS_ACCESS_KEY_ID guard-AWS_SECRET_ACCESS_KEY guard-AWS_REGION guard-PULUMI_ACCESS_TOKEN
	${DOCKER_RUN} -it \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_REGION \
		-e PULUMI_ACCESS_TOKEN \
			${PROJECT_NAME} pulumi destroy --stack ${STACK} ${FLAGS}

recreate: destroy up

clean: docker-images-remove
