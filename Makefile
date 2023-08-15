requirements:
	pipenv requirements --dev > requirements.txt

format:
	black main.py src/ tests/

lint:
	flake8 main.py src/ tests/ --max-line-length 100
	pydocstyle main.py src/ tests/

test:
	pytest -v tests/ --cov=src/ --cov-report term-missing

unit-test:
	pytest -q tests/unit/ --cov=src/ --cov-report term-missing

integration-test:
	pytest -q tests/integration/ --cov=src/ --cov-report term-missing

acceptance-test:
	pytest -q tests/acceptance/ --cov=src/ --cov-report term-missing

coverage:
	pytest -v tests/ --cov=src/ --cov-report term-missing
	coverage html
	coverage xml
	coverage report

clean:
	rm -rf .coverage .pytest_cache build/ dist/ Lyzer-ETL.spec coverage.xml htmlcov/

build:
	pyinstaller \
	--onefile \
	--name=Lyzer-ETL \
	--clean \
	--distpath=dist/ \
	--add-data "version.txt:." \
	main.py