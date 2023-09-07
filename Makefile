resolve:
	pip install -r requirements.txt --upgrade

check-style:
	flake8 --max-complexity 12 flask_classful.py || exit 0
	pylint --rcfile .pylintrc flask_classful.py || exit 0

test-clean:
	coverage erase

test-intg:
	coverage run --branch --source=. -m pytest

test: | test-clean test-intg

report-coverage:
	coverage report --omit=test_classful/*,test_classful_py3/*

.DEFAULT_GOAL := resolve

.PHONY: resolve, check-style, report-coverage, test-clean, test-intg, test
