# Server

Server is a project that aims to be a web server responsible for handling HTTP requests.

## Topics

* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)

## Running locally

Build the docker image:

```sh
make build
```

Set the following environment variables in a `.env` file:

> *`MEIDA_PROVIDER` credentials are specified on the [libs/media-tools/](../../libs/media-tools/README.md#requirements) documentation.*

```sh
MEDIA_PROVIDER_CLIENT_ID=
MEDIA_PROVIDER_CLIENT_SECRET=
```

Export the environment variables:

```sh
export $(cat .env)
```

Run the server:

> The server will be available on http://0.0.0.0:80.

```sh
make server
```

Optionally, run bash within the docker image:

```sh
make shell
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
