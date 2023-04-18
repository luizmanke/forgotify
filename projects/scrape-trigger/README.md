# Scrape Trigger

Scrape Trigger is a project that aims to start the data collection process.

## Topics

* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Pushing image](#pushing-image)
* [Cleaning the workspace](#cleaning-the-workspace)

## Running locally

Build the docker image:

```sh
make build
```

Run bash within the docker image with its database:

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

## Pushing image

Push image to the registry:

```sh
make push
```

## Cleaning the workspace

Ensure the server is not running:

```sh
make stop
```

Remove the docker image:

```sh
make clean
```
