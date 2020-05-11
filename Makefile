.PHONY: test isort isort-check black black-check format lint

PACKAGE_NAME=red_dead

# Test

flake8:
	flake8 $(PACKAGE_NAME) tests

isort:
	isort -rc --atomic $(PACKAGE_NAME) tests $(ARGS)

isort-check:
	$(MAKE) isort ARGS='--check-only --diff'

black:
	black $(PACKAGE_NAME) tests $(ARGS)

black-check:
	$(MAKE) black ARGS='--check --verbose --diff'


format: black isort

lint: flake8 black-check isort-check
