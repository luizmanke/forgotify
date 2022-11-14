# Infra

Infra is a project that holds other projects' infrastructure as code.

It is powered by [Pulumi](https://www.pulumi.com/), which provides built-in state and secrets management, integrates with source control and CI/CD, and offers a web console and API that make it easier to visualize and manage infrastructure.

## Topics

* [Requirements](#requirements)
* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)

## Requirements

* A [Pulumi Account](https://www.pulumi.com/docs/intro/pulumi-service/) with a [Pulumi Access Token](https://www.pulumi.com/docs/intro/pulumi-service/organization-access-tokens/) to manage deployments.

* An [AWS Account](https://aws.amazon.com/free) with an [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) to place the infrastructure.

## Running locally

Build the docker image:

```sh
make build
```

Set the environment variables in a `.env` file to enable connection to the Pulumi Server and the AWS Cloud:

> *References: [AWS Access Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) and [Pulumi Access Token](https://www.pulumi.com/docs/intro/pulumi-service/organization-access-tokens/).*

```sh
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=

PULUMI_ACCESS_TOKEN=
```

Export the environment variables:

```sh
export $(cat .env)
```

Update remote infrastructure:

```sh
make up
```

Optionally, the stack and/or Pulumi flags can be passed as arguments:

```sh
make up STACK=dev FLAGS="--skip-preview"
```

Optionally, run bash within the docker image:

```sh
make shell
```

## Testing locally

Build the docker image:

```sh
make build
```

Lint files (flake8, mypy and bandit):

```sh
make lint
```

Test functionalities:

> Currently, tests were not implemented, given that simplicity of the infrastructure.

```sh
make test
```

Alternatively, the following is an all-in-one command to build, lint and test:

```sh
make all
```

## Cleaning the workspace

Remove the docker image:

```sh
make clean
```
