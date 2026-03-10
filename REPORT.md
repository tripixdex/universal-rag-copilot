# Stage 3.1 Report: Micro-Polish for Demo/Ops Ergonomics

## What changed
- Added `GET /` redirect to `/ui` (status `307`).
- Added explicit `HEAD /ui` returning `200`, `Content-Type: text/html`, and empty body.
- Kept existing `GET /ui` HTML behavior unchanged.
- Added low-noise icon routes to avoid common browser 404 noise:
  - `GET /favicon.ico` -> `204`
  - `GET /apple-touch-icon.png` -> `204`
  - `GET /apple-touch-icon-precomposed.png` -> `204`
- Added API tests for:
  - `GET /` redirect location
  - `HEAD /ui` success/content type/empty body
- Added Makefile ops helpers:
  - `make up` (PID file: `.tmp/api.pid`, log: `.tmp/api.log`, waits for `/health`)
  - `make down` (stops tracked PID only)
  - `make status` (PID tracking + health probe)
  - `make open-ui` (macOS `open` to `/ui`)
- `make up` now refuses to start if `127.0.0.1:8000` is already occupied, exits non-zero, and does not kill unrelated processes.

## Files changed
- `src/universal_rag_copilot/api/app.py`
- `tests/test_api.py`
- `Makefile`
- `REPORT.md`

## Commands run and outputs
### `make format`
```text
python -m ruff format src tests
26 files left unchanged
```

### `make lint`
```text
python -m ruff check src tests
All checks passed!
```

### `make test`
```text
python -m pytest -q
.............                                                            [100%]
13 passed in 0.13s
```

### Additional smoke check
`make up` while port `8000` was already in use:
```text
Port 8000 on 127.0.0.1 is already in use. Refusing to start API.
make: *** [up] Error 1
```

## Remaining limitations
- `make open-ui` uses macOS `open`; on non-macOS systems this target exits with a clear error.
- `make status` checks `/health`; if another process owns port `8000`, it may report unhealthy even though the port is occupied (expected behavior, since PID is not tracked by this project).
