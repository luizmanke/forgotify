# Pipelines

Pipelines is a project that aims to orchestrate the execution of jobs, such as a job that periodically populates a database.

## Important Notes

1. This project is powered by [Dagster](https://dagster.io/), which enables a serverless deployment to orchestrate jobs without spinning up any infrastructure.

2. Tests were not implemented since they would be redundant, given the simplicity of the current pipelines.

## How to run locally

Build the docker image:

```sh
make build
```

Some pipelines require environment variables to work properly. Set them in a `.env` file:

```sh
MEDIA_TOOLS_CLIENT_ID=
MEDIA_TOOLS_CLIENT_SECRET=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USERNAME=
POSTGRES_PASSWORD=
POSTGRES_DATABASE=
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

Optionally, remove the docker image:

```sh
make clean
```

## How to lint locally

Lint files (flake8, mypy and bandit):

```sh
make lint
```

Alternatively, the following is an all-in-one command to build and lint:

```sh
make all
```
