#!/bin/sh

pipenv run flask db upgrade
pipenv run python seeder.py
pipenv run flask run -h 0.0.0.0
