PHONY: lint

lint:
	black --check --line-length 100 .
	pylint --disable=invalid-name,logging-too-many-args,logging-format-interpolation,invalid-overridden-method,bad-continuation CCC_Bot.py ./utils/ ./cogs/
	flake8 CCC_Bot.py ./utils/ ./cogs/ --statistics --show-source --max-line-length 100
	bandit -r ./CCC_Bot.py ./cogs/ ./utils/