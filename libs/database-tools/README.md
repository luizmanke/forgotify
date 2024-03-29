# Database Tools

Database Tools is a package that aims to ease operations to databases, such as reading and writing.

## Topics

* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)
* [Adding this project as a dependency](#adding-this-project-as-a-dependency)

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

## Adding this project as a dependency

Add the the following line to the project's `pyproject.toml`:

```
[tool.poetry.dependencies]
...
database-tools = { path = "../../libs/database-tools", extras = ["storage"] }
```

> *Where `extras` are the required database-tools subpackages: postgres, storage, ...*
