PHONY: lint reformat

lint:
	black --check --line-length 100 ./CCC_Bot.py ./cogs/ ./utils/
	pylint CCC_Bot.py ./utils/ ./cogs/
	flake8 CCC_Bot.py ./utils/ ./cogs/ --statistics --show-source --max-line-length 100
	bandit -r ./CCC_Bot.py ./cogs/ ./utils/

reformat:
	black --line-length 100 ./CCC_Bot.py ./cogs/ ./utils/