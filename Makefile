PIP ?= pip
PYTHON ?= python

SOURCES = pfm examples main.py
TESTS = tests

install:
	$(PIP) install --upgrade --no-cache-dir pip -r requirements-dev.txt

test:
	$(PYTHON) -m unittest -qvb

cov:
	coverage run --source pfm -m unittest -qvb
	coverage report
	coverage html -d coverage/html
	coverage xml -o coverage/cobertura.xml
	coverage erase

isort:
	isort -rc $(SOURCES) $(TESTS)

mypy:
	mypy $(SOURCES)

pylint:
	pylint $(SOURCES)

flake:
	flake8 $(SOURCES)

lint: isort mypy pylint flake test

all: install lint cov

.PHONY: install test cov isort mypy pylint flake lint all

.DEFAULT_GOAL := all
