PHONY: lint format

lint:
	black --check --line-length 100 ./bot
	pylint ./bot
	flake8 ./bot --statistics --show-source --max-line-length 100
	bandit -r ./bot

format:
	black --line-length 100 ./bot