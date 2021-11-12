#! /usr/bin/bash

autoflake --in-place --recursive reactant && isort reactant tests && black reactant tests \
&& echo "Files now autoflaked, isorted, and black formatted."