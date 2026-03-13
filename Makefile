.PHONY: format lint test tree up down status open-ui

API_HOST ?= 127.0.0.1
API_PORT ?= 8000
API_URL := http://$(API_HOST):$(API_PORT)
LOCAL_PYTHONPATH ?= src
PID_FILE := .tmp/api.pid
LOG_FILE := .tmp/api.log

format:
	python -m ruff format src tests

lint:
	python -m ruff check src tests

test:
	python -m pytest -q

tree:
	@find . -maxdepth 3 -type d | sort

up:
	@mkdir -p .tmp
	@if [ -f "$(PID_FILE)" ] && kill -0 "$$(cat "$(PID_FILE)")" 2>/dev/null; then \
		echo "API already running (PID $$(cat "$(PID_FILE)"))."; \
		exit 0; \
	fi
	@if [ -f "$(PID_FILE)" ]; then rm -f "$(PID_FILE)"; fi
	@python -c "import socket,sys; s=socket.socket(); code=s.connect_ex(('$(API_HOST)', $(API_PORT))); s.close(); sys.exit(1 if code == 0 else 0)" || { \
		echo "Port $(API_PORT) on $(API_HOST) is already in use. Refusing to start API."; \
		exit 1; \
	}
	@PYTHONPATH="$(LOCAL_PYTHONPATH)" python -m universal_rag_copilot.api.app >"$(LOG_FILE)" 2>&1 & echo $$! >"$(PID_FILE)"
	@for i in $$(seq 1 30); do \
		if curl -sSf "$(API_URL)/health" >/dev/null; then \
			echo "API is up at $(API_URL) (PID $$(cat "$(PID_FILE)"))."; \
			exit 0; \
		fi; \
		sleep 1; \
	done; \
	echo "API did not become healthy in time. See $(LOG_FILE)."; \
	kill "$$(cat "$(PID_FILE)")" 2>/dev/null || true; \
	rm -f "$(PID_FILE)"; \
	exit 1

down:
	@if [ ! -f "$(PID_FILE)" ]; then \
		echo "API is not running (no PID file)."; \
		exit 0; \
	fi
	@pid="$$(cat "$(PID_FILE)")"; \
	if kill -0 "$$pid" 2>/dev/null; then \
		kill "$$pid"; \
		echo "Stopped API (PID $$pid)."; \
	else \
		echo "Removed stale PID file (PID $$pid not running)."; \
	fi; \
	rm -f "$(PID_FILE)"

status:
	@if [ -f "$(PID_FILE)" ] && kill -0 "$$(cat "$(PID_FILE)")" 2>/dev/null; then \
		echo "API PID file present: $$(cat "$(PID_FILE)")"; \
	else \
		echo "API PID not tracked."; \
	fi
	@if curl -sSf "$(API_URL)/health" >/dev/null; then \
		echo "Health: ok ($(API_URL)/health)"; \
	else \
		echo "Health: unavailable ($(API_URL)/health)"; \
	fi

open-ui:
	@command -v open >/dev/null 2>&1 || { echo "'open' command not found on this system."; exit 1; }
	@open "$(API_URL)/ui"
