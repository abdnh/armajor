.PHONY: all test format checkformat typecheck lint check clean zip ankiweb run

all: ankiweb zip

zip:
	python -m ankibuild --type package --install --qt all

ankiweb:
	python -m ankibuild --type ankiweb --install --qt all

run: zip
	python -m ankirun

test:
	python -m pytest

format:
	python -m black src

checkformat:
	python -m black --diff --color src

typecheck:
	python -m mypy src

lint:
	python -m pylint src

check: lint typecheck checkformat

clean:
	rm -rf build/
