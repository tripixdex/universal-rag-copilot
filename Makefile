.PHONY: format lint test tree

format:
	@echo "Placeholder: run code formatter (to be defined in next stage)."

lint:
	@echo "Placeholder: run linters (to be defined in next stage)."

test:
	@echo "Placeholder: run tests (to be defined in next stage)."

tree:
	@find . -maxdepth 3 -type d | sort
