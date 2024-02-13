# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Include my.env and export it so variables set in there are available
# in the Makefile.
include .env
export

DOCKER := $(shell which docker)
DC=${DOCKER} compose

.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "Usage: make RULE"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile \
		| grep -v grep \
	    | sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	    | column -t  -s '|'
	@echo ""
	@echo "Adjust your .env file to set configuration."
	@echo ""
	@echo "See https://mozilla-eliot.readthedocs.io/ for more documentation."

# Dev configuration steps
.docker-build:
	make build

.devcontainer-build:
	make devcontainerbuild

.env:
	./bin/cp-env-file.sh

.PHONY: build
build: .env  ## | Build docker images.
	${DC} build --progress plain base
	${DC} build --progress plain fakesentry statsd
	touch .docker-build

.PHONY: run
run: .env .docker-build  ## | Run eliot and services.
	${DC} up \
		--attach eliot \
		--attach fakesentry \
		eliot fakesentry

.PHONY: devcontainerbuild
devcontainerbuild: .env .docker-build .devcontainer-build  ## | Build VS Code development container.
	${DC} build --progress plain devcontainer
	touch .devcontainer-build

.PHONY: devcontainer
devcontainer: .env .docker-build  ## | Run VS Code development container.
	${DC} up --detach devcontainer

.PHONY: stop
stop: .env  ## | Stop docker containers.
	${DC} stop

.PHONY: shell
shell: .env .docker-build  ## | Open a shell in eliot service container.
	${DC} run --rm eliot bash

.PHONY: clean
clean: .env stop  ## | Stop and remove docker containers and artifacts.
	${DC} rm -f
	rm -fr .docker-build

.PHONY: test
test: .env .docker-build  ## | Run Python unit test suite.
	${DC} up -d fakesentry statsd
	${DC} run --rm test bash ./bin/run_test.sh

.PHONY: testshell
testshell: .env .docker-build  ## | Open shell in test environment.
	${DC} up -d fakesentry statsd
	${DC} run --rm test bash ./bin/run_test.sh --shell

.PHONY: docs
docs: .env .docker-build  ## | Build docs.
	${DC} run --rm --no-deps eliot bash make -C docs/ clean
	${DC} run --rm --no-deps eliot bash make -C docs/ html

.PHONY: lint
lint: .env .docker-build  ## | Lint code.
	${DC} run --rm --no-deps test bash ./bin/run_lint.sh

.PHONY: lintfix
lintfix: .env .docker-build  ## | Reformat code.
	${DC} run --rm --no-deps test bash ./bin/run_lint.sh --fix

.PHONY: rebuildreqs
rebuildreqs: .env .docker-build  ## | Rebuild requirements.txt file after requirements.in changes.
	${DC} run --rm --no-deps eliot bash pip-compile --generate-hashes

.PHONY: updatereqs
updatereqs: .env .docker-build  ## | Update deps in requirements.txt file.
	${DC} run --rm --no-deps eliot bash pip-compile --generate-hashes -U
