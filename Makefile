.PHONY: all forms test build format check clean

all: build

forms: src/dialog.py

src/dialog.py: designer/dialog.ui 
	pyuic5 $^ > $@

build: forms

test:
	cd src && python test.py

format:
	python -m black $(wildcard src/*.py)

check:
	python -m pylint $(filter-out src/dialog.py, $(wildcard src/*.py))

zip: build.zip

build.zip: src/*
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f src/dialog.py
	rm -f build.zip
