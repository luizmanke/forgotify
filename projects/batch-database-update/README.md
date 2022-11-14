# Batch Database Update

Batch Database Update is a project that aims to update the media database as a batch process.

## Topics

* [Requirements](#requirements)
* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Creating migrations](#creating-migrations)
* [Applying migrations](#applying-migrations)
* [Cleaning the workspace](#cleaning-the-workspace)

## Requirements

The following environment variables are required:

> *`MEIDA_PROVIDER` credentials are specified on the [libs/media-tools/](../../libs/media-tools/README.md#requirements) documentation.*

```sh
DATABASE_HOST=
DATABASE_PORT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=

MEDIA_PROVIDER_CLIENT_ID=
MEDIA_PROVIDER_CLIENT_SECRET=
```

*Note: Database environment variables are only required when working with a remote server. For local runs, these values are already set in the [docker-compose file](./docker-compose.yml)*

## Running locally

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

## Creating migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/en/latest/), which is a lightweight database migration tool for SQLAlchemy.

Create a new revision:

```sh
make migrations-revision
```

After running the previous command, a new revision should be available in the [migrations/versions/](./migrations/versions/) folder.

## Applying migrations

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

## Cleaning the workspace

Stop containers, remove containers, and remove the docker image:

```sh
make clean
```
