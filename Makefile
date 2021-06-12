PHONY: lint reformat

lint:
	black --check --line-length 100 ./bot
	pylint ./bot
	flake8 ./bot --statistics --show-source --max-line-length 100
	bandit -r ./bot

reformat:
	black --line-length 100 ./bot