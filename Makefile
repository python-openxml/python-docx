BEHAVE = behave
MAKE   = make
PYTHON = python
SETUP  = $(PYTHON) ./setup.py

.PHONY: accept clean coverage docs readme register sdist test upload

help:
	@echo "Please use \`make <target>' where <target> is one or more of"
	@echo "  accept    run acceptance tests using behave"
	@echo "  clean     delete intermediate work product and start fresh"
	@echo "  cleandocs delete intermediate documentation files"
	@echo "  coverage  run nosetests with coverage"
	@echo "  docs      generate documentation"
	@echo "  opendocs  open browser to local version of documentation"
	@echo "  register  update metadata (README.rst) on PyPI"
	@echo "  sdist     generate a source distribution into dist/"
	@echo "  upload    upload distribution tarball to PyPI"

accept:
	$(BEHAVE) --stop

clean:
	find . -type f -name \*.pyc -exec rm {} \;
	rm -rf dist *.egg-info .coverage .DS_Store

cleandocs:
	$(MAKE) -C docs clean

coverage:
	py.test --cov-report term-missing --cov=docx tests/

docs:
	$(MAKE) -C docs html

opendocs:
	open docs/.build/html/index.html

register:
	$(SETUP) register

sdist:
	$(SETUP) sdist

upload:
	$(SETUP) sdist upload
