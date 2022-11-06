# Pipelines

Pipelines is a project that aims to orchestrate the execution of jobs, such as a job that periodically populates a database.

It is powered by [Dagster](https://dagster.io/), which enables a serverless deployment to orchestrate jobs without spinning up any infrastructure.

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

## How to test locally

Build the docker image:

```sh
make build
```

Lint files (flake8, mypy and bandit):

```sh
make lint
```

Test functionalities:

> Currently, test were not implemented since they would be redundant, given that the projects used within the pipelines have already been tested.

```sh
make test
```

Alternatively, the following is an all-in-one command to build, lint and test:

```sh
make all
```

## How to clean the workspace

Remove the docker image:

```sh
make clean
```
