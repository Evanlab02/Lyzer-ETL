requirements:
	pipenv requirements --dev > requirements.txt

format:
	black main.py src/

lint:
	flake8 main.py src/ --max-line-length 100
	pydocstyle main.py src/

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