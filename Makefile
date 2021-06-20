.PHONY: all forms test build format checkformat typecheck lint check clean addon zip

all: build

forms: src/dialog.py

src/dialog.py: designer/dialog.ui 
	pyuic5 $^ > $@

build: forms

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

zip: build.zip

build.zip: src/*
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

addon: zip
	cp build.zip armajor.ankiaddon
	cp src/* dev-profile/addons21/armajor

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f src/dialog.py
	rm -f build.zip
	rm -f armajor.ankiaddon
