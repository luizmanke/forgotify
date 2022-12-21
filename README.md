# Forgotify

Forgotify is a service that aims to help people find unpopular songs based on any [Spotify](https://open.spotify.com/) playlist.

## Topics

* [Requirements](#requirements)
* [Changelog](#changelog)

## Requirements

* [Poetry](https://python-poetry.org/) is a tool for dependency management and packaging in Python. Every project in this repository is structured based on this tool.

* [GNU Make](https://www.gnu.org/software/make/) is a software that controls the generation of executables and other non-source files of a program from the program's source files. Every interaction from the user to this project should be through a Makefile, except for poetry and git actions.

* [Docker](https://www.docker.com/) is a platform that uses OS-level virtualization to deliver software in packages called containers. Every command in this repository uses this tool to isolate the running environment.

* [Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. Used in some cases in exchange for the regular Docker command.

## Changelog

Every time a new commit or tag is pushed to the main branch, the [changelog workflow](./.github/workflows/changelog.yml) is triggered.

The workflow uses [Commitizen](https://github.com/commitizen/cz-cli) to automatically update the [CHANGELOG.md](./CHANGELOG.md) file based on the latest commits.

> In order for this to work properly, the commits must follow the [conventinal commits](https://www.conventionalcommits.org/en/v1.0.0/) style.
