python ?= python3.6

pip ?= pip3.6

pytest ?= pytest

pipenv ?= pipenv

mypy ?= mypy

all: setup update test package

setup:
	$(pip) install pipenv

update:
	$(pipenv) sync --dev
	$(pipenv) run $(pip) list

test: pep8 mypy
	$(pipenv) run $(pytest) -v --cov=etchy $(ARGS)

open-cov:
	$(pipenv) run $(pytest) -v --cov=etchy --cov-report=html
	xdg-open htmlcov/index.html

pep8:
	$(pipenv) run flake8 --show-source etchy.py

mypy:
	$(pipenv) run $(mypy) etchy.py || true

fmt:
	$(pipenv) run yapf -i etchy.py tests/test_etchy.py
	$(pipenv) run isort -rc --atomic etchy.py tests/test_etchy.py

shell:
	$(pipenv) shell

binary:
	$(pipenv) run ./scripts/binary.sh

package: binary
	$(pipenv) run ./scripts/package.sh
