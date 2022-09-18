#!/bin/env sh

clear
mypy --strict --pretty "$1"
python3 "$1"
