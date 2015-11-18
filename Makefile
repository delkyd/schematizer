REBUILD_FLAG =

.PHONY: help all production clean docs test debug itest cook-image docker-push install-hooks

help:
	@echo "clean - remove artifacts"
	@echo "debug - run tests and allow interactive breaks on ipbd.set_trace()"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "test - run tests quickly with the default Python"
	@echo "itest - cook the image and do paasta local run acceptance tests"
	@echo "cook-image - only cook the docker image"
	@echo "docker-push - push a new docker image"
	@echo "install-hooks - Install the pre-commit hooks"

all: production install-hooks

production:
	@true

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	rm -rf docs/build/*
	rm -rf .tox/

docs:
	tox -e docs

test:
	tox $(REBUILD_FLAG)

debug:
	tox $(REBUILD_FLAG) -- -s

itest: cook-image
	paasta local-run -s schematizer -t
	tox -e acceptance

DOCKER_TAG ?= schematizer-dev-$(USER)

cook-image:
	docker build -t $(DOCKER_TAG) .

export GIT_SHA ?= $(shell git rev-parse --short HEAD)

docker-push:
	tox -e docker-push

install-hooks:
	tox -e pre-commit -- install -f --install-hooks
