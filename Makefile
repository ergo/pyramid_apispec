# Makefile for local development

SHELL := /bin/bash
export PYTHONUNBUFFERED := 1
export PATH := $(shell echo $$PATH):./bin

PYTHON := $(shell /usr/bin/which python{3.7,3.6})

ifneq (,$(findstring 3.7,$(PYTHON)))
    PY_VERSION := 3.7
endif
ifneq (,$(findstring 3.6,$(PYTHON)))
    PY_VERSION := 3.6
endif
PY_TOX := py$(subst .,,$(PY_VERSION))

PIP := .tox/$(PY_TOX)/bin/pip$(PY_VERSION)

.DEFAULT_GOAL := build


$(PIP): var
	tox -e $(PY_TOX)


.PHONY: build
build: $(PIP) requirements.development.txt
	$(PIP) \
		--isolated \
		--disable-pip-version-check \
		install -r requirements.development.txt

.PHONY: test
test: $(PIP)
	TOXENV=$(PY_TOX) tox


# only for initial build, without having a requirements file in place
.PHONY: build.setup
build.setup: $(PIP)
	$(PIP) \
		--isolated \
		--disable-pip-version-check \
		install .[dev]

requirements.development.txt: build.setup
	cat \
		<($(PIP) freeze \
			| grep -v pyramid-apispec \
			) \
		<(echo '-e .[dev]') \
		> requirements.development.txt

.PHONY: pip.freeze
pip.freeze:
	rm -f requirements.development.txt
	@make clean
	@make build


var:
	mkdir -p ./var

.PHONY: clean
clean: pyc-clean
	rm -rf \
		/.tox

.PHONY: pyc-clean
pyc-clean:
	find ./ -name __pycache__ -exec rm -rf {} \+
	find ./ -name '*.pyc' -exec rm -f {} \+

