app: requirements.txt
	python3.9 -m venv app || (rm -fr app; exit 1)
	app/bin/pip3 install -r requirements.txt

.PHONY: codelint
codelint:
	app/bin/pylint netboxlint $(wildcard org/*.py linter/*.py)
