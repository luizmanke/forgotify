# Batch Database Update

Batch Database Update is a project that aims to update the media database as a batch process.

## Topics

* [Requirements](#requirements)
* [How to run locally](#how-to-run-locally)
* [How to test locally](#how-to-test-locally)
* [How to create migrations](#how-to-create-migrations)
* [How to apply migrations](#how-to-apply-migrations)
* [How to clean the workspace](#how-to-clean-the-workspace)

## Requirements

To work with a remote server, the following environment variables are required:

> *Local runs doesn't require any environment variable.*

```sh
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=

MEDIA_PROVIDER_CLIENT_ID=
MEDIA_PROVIDER_CLIENT_SECRET=
```

The `MEIDA_PROVIDER` credentials are specified on the [libs/media-tools/](../../libs/media-tools/README.md#requirements) documentation.

## How to run locally

Build the docker image:

```sh
make build
```

Run bash within the docker image:

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

## How to create migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/en/latest/), which is a lightweight database migration tool for SQLAlchemy.

Create a new revision:

```sh
make migrations-revision
```

After running the previous command, a new revision should be available in the [migrations/versions/](./migrations/versions/) folder.

## How to apply migrations

> *Migrations are automatically applied to local databases when running tests or shell.*

Set the environment variables in a `.env` file:

```sh
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=
```

Export the environment variables:

```sh
export $(cat .env)
```

Apply migrations:

```sh
make migrations-apply-remote
```

## How to clean the workspace

Stop containers, remove containers, and remove the docker image:

```sh
make clean
```
