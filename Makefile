PHONY: lint format pg-proxy build deploy deploy-prod

lint:
	black --check --line-length 100  --target-version py311 ./bot
	pylint --py-version 3.11 ./bot
	flake8 ./bot --statistics --show-source --max-line-length 100
	bandit -r ./bot

format:
	black --line-length 100 --target-version py311 ./bot

pg-proxy:
	flyctl proxy 5432 -a ccc-postgres

build:
	flyctl deploy --local-only --build-only

deploy:
	flyctl deploy --local-only

deploy-prod:
	flyctl deploy --local-only --app ccc-bot