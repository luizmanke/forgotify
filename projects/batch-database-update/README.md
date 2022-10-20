# Batch Database Update

Batch Database Update is a project that aims to update the media database as a batch process.

## How to run locally

Build the docker image:

```sh
make build
```

Run Python within the docker image:

```sh
make shell
```

Stop the server when done using it:

```sh
make stop
```

## How to test locally

Lint files (flake8, mypy and bandit):

```sh
make lint
```

Test functionalities:

```sh
make test
```

Alternatively, the following is an all-in-one command to build, lint and test:

```sh
make all
```

## How to use migrations

Create a new revision:

```sh
make migrations-revision
```

*Migrations are automatically applied when running tests or shell.*