# Makefile for 'thebigselector'

.RECIPEPREFIX= :

.PHONY: pkg publish clean doc

pkg: clean doc
#: python3 -m pip install --user --upgrade setuptools wheel
: python3 setup.py sdist bdist_wheel


README.md: docs/_pdREADME.md
: pandoc -t gfm -o $@ $<

docs/Use.md: docs/_pdUse.md
: pandoc -t gfm -o $@ $<

docs/Use.html: docs/_pdUse.md
: pandoc -s --quiet -o $@  $<

doc: README.md docs/Use.md docs/Use.html


publish: pkg
# Publishing to PyPi
#: python3 -m pip install --user --upgrade twine
#: python3 -m twine upload --repository testpypi dist/*
: python3 -m twine upload --repository pypi dist/*

clean:
: rm -fr build dist *.egg-info
