# Database Tools

Database Tools is a package that aims to ease operations to databases, such as reading and writing.

Currently, it supports:

* [Postgres](https://www.postgresql.org/)

## Topics

* [How to run locally](#how-to-run-locally)
* [How to test locally](#how-to-test-locally)
* [How to clean the workspace](#how-to-clean-the-workspace)

## How to run locally

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

## How to clean the workspace

Stop containers, remove containers, and remove the docker image:

```sh
make clean
```
