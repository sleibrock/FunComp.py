shell:
	python -i Unit/All.py 
ishell:
	ipython -i Unit/All.py
test:
	python Unit/tests.py
install:
	python setup.py install
build:
	python setup.py sdist bdist_wheel
upload:
	twine upload dist/*
