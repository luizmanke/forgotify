# Media Tools

Media Tools is a package that aims to ease the search for all kinds of media, such as songs, artists, and playlists.

It is powered by [Spotify](https://open.spotify.com/), which is one of the largest music streaming service providers.

## Topics

* [Requirements](#requirements)
* [Running locally](#running-locally)
* [Testing locally](#testing-locally)
* [Cleaning the workspace](#cleaning-the-workspace)

## Requirements

Media Tools requires a `client_id` and a `client_secret`. These values can be acquired at [Spotify dashboard](https://developer.spotify.com/dashboard/).

## Running locally

Build the docker image:

```sh
make build
```

Run bash within the docker image:

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

Remove the docker image:

```sh
make clean
```
