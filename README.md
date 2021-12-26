# Training: External Dependencies

The intent of this repo is to serve as a source of data when learning a programming language, framework, or other
training related exercises. This allows me (and others) to reduce the time needed to setup dependencies.

# Setup

To generate the needed data then run the following steps:

1. run: `./build.sh -cd`
2. run: `docker-compose up -d`

Note:
The `-d` flag for `docker-compose up` is optional

## Build Script

The build script can be used with the following:

- No Arguments - The script will build with docker (no new data or teardown)
- `-c`: The script will pass the `--no-cache` argument to Docker, which prevents the usage of caching
- `-d`: The script will do a tear down, which runs `docker-compose down` and re-ingests the sample data BEFORE
  building with docker

## Dependencies

The repo is using Python 3.8 to generate the data. In addition, the shell scripts was implemented on Unix.

#  Python Data Generation

Sample files were pulled from [PushShift](https://files.pushshift.io/). When running the python scripts to ingest, it will
follow 2 different paths.

## Postgres
The script will walk over the [sample files](./data) and will create new SQL files with **each line** converted
to the appropriate translation AND a prefix for the database table connection in the [source data folder](./postgres/data). 

When all the data files have been created, cleanup will occur by removing unnecessary files.


## Elasticsearch
The script will walk over the [sample files](./data) and will create new JSON files with **each line** being prefixed with
index information needed by Elasticsearch. The files are located within the [source data folder](./elasticsearch/data).

When all the data files have been created, cleanup will occur by converting the files from JSON (JSON Lines) to GZIP.