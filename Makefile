PHONY: lint format pg-proxy

lint:
	black --check --line-length 100 ./bot
	pylint ./bot
	flake8 ./bot --statistics --show-source --max-line-length 100
	bandit -r ./bot

format:
	black --line-length 100 ./bot

pg-proxy:
	flyctl proxy 5432 -a ccc-postgres

deploy:
	flyctl deploy --local-only

deploy-prod:
	flyctl deploy --local-only --app ccc-bot