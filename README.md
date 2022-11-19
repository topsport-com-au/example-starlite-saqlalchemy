# example-starlite-saqlalchemy

<img src="https://www.topsport.com.au/assets/images/logo_pulse.svg" width="200"/>

Example API built on [starlite-saqlalchemy](https://topsport-com-au.github.io/starlite-saqlalchemy/latest/)

## Setup

- `$ poetry install`
- `$ cp .env.example .env`
- `$ docker-compose up -d`
- `$ poetry run alembic upgrade head`

## Run

`$ poetry run run-app`

## Development

Install dev dependencies:

`$ python -m pip install -r dev.requirements.txt`

## Test

`$ tox`

## Migrations

### Ensure the database service is up

`$ docker-compose up -d`

### Revision

`$ poetry run alembic revision --autogenerate -m "revision description"`

### Migration

`$ poetry run alembic upgrade head`
