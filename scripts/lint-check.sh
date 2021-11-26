#! /usr/bin/sh

flake8 reactant tests
black reactant tests --check
isort reactant tests --check-only