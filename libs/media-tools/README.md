# Media Tools

Media Tools is a package that aims to ease the search for all kinds of media, such as songs, artists, and playlists.

It is powered by [Spotify](https://open.spotify.com/), which is one of the largest music streaming service providers.

## Topics

* [Requirements](#requirements)
* [How to run locally](#how-to-run-locally)
* [How to test locally](#how-to-test-locally)
* [How to clean the workspace](#how-to-clean-the-workspace)

## Requirements

Media Tools requires a `client_id` and a `client_secret`. These values can be acquired at [Spotify dashboard](https://developer.spotify.com/dashboard/).

## How to run locally

Build the docker image:

```sh
make build
```

Run bash within the docker image:

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

## How to clean the workspace

Remove the docker image:

```sh
make clean
```
