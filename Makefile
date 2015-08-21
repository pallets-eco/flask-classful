resolve:
	pip install -r requirements.txt --upgrade

check-style:
	flake8 --max-complexity 12 . || exit 0
	pylint --rcfile .pylintrc *.py **/*.py **/**/*.py **/**/**/*.py || exit 0

test-clean:
	coverage erase

test-intg:
	coverage run --branch --source=. `which nosetests` -v --exe

test: | test-clean test-intg

report-coverage:
	coverage report --omit=test_classy/*,setup.py

.DEFAULT_GOAL := resolve

.PHONY: resolve, check-style, report-coverage, test-clean, test-intg, test
