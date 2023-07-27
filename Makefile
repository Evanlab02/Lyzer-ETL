requirements:
	pipenv requirements --dev > requirements.txt

format:
	black src/ tests/

lint:
	flake8 src/ tests/ --max-line-length 100
	pydocstyle src/ tests/

test:
	pytest -v tests/ --cov=src/ --cov-report term-missing

clean:
	rm -rf .coverage .pytest_cache build/ dist/ Lyzer-Hydrate.spec

build:
	pyinstaller --onefile --name=Lyzer-Hydrate --clean --distpath=dist/ src/main.py