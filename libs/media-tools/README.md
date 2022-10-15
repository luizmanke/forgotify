# Media Tools

Media Tools is a package that aims to ease the search for all kinds of media, such as songs, artists, and playlists.

## How to run locally

Build the docker image:

```sh
make build
```

Run Python within the docker image:

```sh
make shell
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
