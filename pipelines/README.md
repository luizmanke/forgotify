# Pipelines

Pipelines is a project that aims to orchestrate the execution of jobs, such as a job that periodically populates a database.

It is powered by [Dagster](https://dagster.io/), which enables a serverless deployment to orchestrate jobs without spinning up any infrastructure.

## Topics

* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)

## Running locally

Build the docker image:

```sh
make build
```

Some pipelines require environment variables to work properly. Set them in a `.env` file:

> *Go to the project directory to check the required environment variables.*

```sh
ENVIRONMENT_VARIABLE_1=value-1
ENVIRONMENT_VARIABLE_2=value-2
...
```

Export the environment variables:

```sh
export $(cat .env)
```

Run the server:

> The server will be available on http://0.0.0.0:3000.

```sh
make server
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

> Currently, tests were not implemented since they would be redundant, given that the projects used within the pipelines have already been tested.

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
