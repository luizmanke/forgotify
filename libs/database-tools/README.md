# Database Tools

Database Tools is a package that aims to ease operations to databases, such as reading and writing.

Currently, it supports:

* [Postgres](https://www.postgresql.org/)

## Topics

* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)

## Running locally

> *The project makes use of docker-compose to start local databases.*

Build the docker image:

```sh
make build
```

Run bash within the docker image with its database:

```sh
make shell
```

Stop the server when done using it:

```sh
make stop
```

## Testing locally

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

## Cleaning the workspace

Stop containers, remove containers, and remove the docker image:

```sh
make clean
```
