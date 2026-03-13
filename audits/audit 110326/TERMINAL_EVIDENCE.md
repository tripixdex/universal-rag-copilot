# TERMINAL EVIDENCE

## Exact commands run
```text
pwd
find . -maxdepth 2 -type d | sort
rg --files
rg --files -g 'README*' -g 'SCOPE*' -g 'ACCEPTANCE*' -g 'DEMO*' -g 'REPORT*' -g 'AUDIT*'
sed -n '1,220p' README.md
sed -n '1,240p' docs/SCOPE.md
sed -n '1,240p' docs/ACCEPTANCE_CRITERIA.md
sed -n '1,240p' docs/DEMO_SCENARIOS.md
sed -n '1,240p' REPORT.md
sed -n '1,260p' AUDIT_EXPERT_REPORT.md
sed -n '1,220p' Makefile
sed -n '1,260p' pyproject.toml
nl -ba src/universal_rag_copilot/pipeline.py | sed -n '1,260p'
nl -ba src/universal_rag_copilot/ingestion/local_ingestion.py | sed -n '1,260p'
nl -ba src/universal_rag_copilot/chunking/strategies.py | sed -n '1,320p'
nl -ba src/universal_rag_copilot/retrieval/baseline.py | sed -n '1,280p'
nl -ba src/universal_rag_copilot/retrieval/pipeline.py | sed -n '1,320p'
nl -ba src/universal_rag_copilot/answering/composer.py | sed -n '1,260p'
nl -ba src/universal_rag_copilot/ui/cli.py | sed -n '1,340p'
nl -ba src/universal_rag_copilot/api/app.py | sed -n '1,360p'
nl -ba src/universal_rag_copilot/api/ui_page.py | sed -n '1,360p'
nl -ba src/universal_rag_copilot/evaluation/runner.py | sed -n '1,360p'
nl -ba tests/test_api.py | sed -n '1,320p'
nl -ba tests/test_retrieval_answering.py | sed -n '1,320p'
nl -ba tests/test_evaluation_runner.py | sed -n '1,320p'
nl -ba tests/test_chunking.py | sed -n '1,260p'
nl -ba fixtures/eval/cases.json | sed -n '1,320p'
nl -ba src/universal_rag_copilot/domain/models.py | sed -n '1,260p'
nl -ba src/universal_rag_copilot/config.py | sed -n '1,220p'
sed -n '1,240p' docs/EVAL_PLAN.md
git status --short
make lint
make test
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How long do card refunds take to settle?"
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode support_kb --profile balanced --question "How do I renew a passport in Canada?"
PYTHONPATH=src python -m universal_rag_copilot.ui.cli run-eval
make up
sed -n '1,220p' .tmp/api.log
make status
ls -la .tmp
cat .tmp/api.pid
ps -p $(cat .tmp/api.pid) -o pid,ppid,stat,command
zsh
PYTHONPATH=src python -m universal_rag_copilot.api.app > .tmp/live_audit.log 2>&1 &
sed -n '1,120p' .tmp/live_audit.log
/bin/zsh -lc "mkdir -p .tmp && PYTHONPATH=src uvicorn universal_rag_copilot.api.app:app --host 127.0.0.1 --port 8011 > .tmp/audit_api.log 2>&1 & echo $!"
curl -sS http://127.0.0.1:8011/health
curl -sSI http://127.0.0.1:8011/ui
curl -sS http://127.0.0.1:8011/ask -X POST -H 'content-type: application/json' -d '{"mode":"support_kb","profile":"balanced","question":"How long do card refunds take to settle?"}'
curl -sS http://127.0.0.1:8011/run-eval -X POST -H 'content-type: application/json' -d '{}'
sed -n '1,200p' .tmp/audit_api.log
PYTHONPATH=src python - <<'PY'
from fastapi.testclient import TestClient
from universal_rag_copilot.api.app import app
client = TestClient(app)
print('GET /health', client.get('/health').status_code, client.get('/health').json())
resp = client.post('/ask', json={'mode':'support_kb','profile':'balanced','question':'How long do card refunds take to settle?','top_k':4,'min_score_threshold':0.07,'min_evidence_results':1})
print('POST /ask answerable', resp.status_code, resp.json()['answerability'], len(resp.json()['citations']))
resp = client.post('/ask', json={'mode':'support_kb','profile':'balanced','question':'How do I renew a passport in Canada?'})
print('POST /ask insufficient', resp.status_code, resp.json()['answerability'], len(resp.json()['citations']))
resp = client.post('/ask', json={'mode':'support_kb','profile':'balanced','question':'x'*401})
print('POST /ask long question', resp.status_code)
resp = client.post('/run-eval', json={})
body = resp.json()
print('POST /run-eval', resp.status_code, body['total_cases'], body['passed_cases'])
resp = client.post('/run-eval', json={'output_dir':'../escape'})
print('POST /run-eval extra field', resp.status_code)
PY
sed -n '1,220p' outputs/eval/eval_20260311T183409Z.json
sed -n '1,220p' outputs/eval/eval_20260311T183409Z.md
sed -n '1,220p' docs/PRD.md
sed -n '1,220p' docs/ARCHITECTURE.md
sed -n '1,220p' docs/PROJECT_MAP.md
nl -ba README.md | sed -n '1,260p'
nl -ba docs/SCOPE.md | sed -n '1,220p'
nl -ba docs/ACCEPTANCE_CRITERIA.md | sed -n '1,240p'
nl -ba docs/DEMO_SCENARIOS.md | sed -n '1,260p'
nl -ba docs/EVAL_PLAN.md | sed -n '1,260p'
nl -ba docs/ARCHITECTURE.md | sed -n '1,260p'
nl -ba REPORT.md | sed -n '1,280p'
nl -ba AUDIT_EXPERT_REPORT.md | sed -n '1,320p'
PYTHONPATH=src python -m universal_rag_copilot.ui.cli index-demo --mode academic_pdf --profile coarse
PYTHONPATH=src python -m universal_rag_copilot.ui.cli ask-demo --mode academic_pdf --profile balanced --question "In batch gradient descent, what data does each step use?"
nl -ba src/universal_rag_copilot/__main__.py | sed -n '1,120p'
```

## Concise outputs
- `make lint`
  - `python -m ruff check src tests`
  - `All checks passed!`
- `make test`
  - `python -m pytest -q`
  - `19 passed in 0.12s`
- `git status --short`
  - Dirty worktree with modified source/docs/tests and untracked prior audit artifacts.
- `ask-demo` support answerable
  - `Refunds to cards usually settle in 5 - 10 business days.`
  - `Answerability: answerable`
  - Citation: `Returns and Refunds`
- `ask-demo` support unanswerable
  - `Not enough evidence in the indexed corpus to answer this question reliably.`
  - `Answerability: not_enough_evidence`
  - `Citations: none`
- `run-eval`
  - Wrote `outputs/eval/eval_20260311T183409Z.json`
  - Wrote `outputs/eval/eval_20260311T183409Z.md`
- Latest eval JSON
  - `total_cases: 18`
  - `passed_cases: 18`
- `index-demo`
  - `Indexed mode=academic_pdf profile=coarse: documents=3 chunks=9`
- `ask-demo` academic
  - Returned `answerable`
  - Included relevant first citation `Optimization for Machine Learning`
  - Also included irrelevant `Neural Networks Basics` snippets in the same answer
- `make up`
  - `API is up at http://127.0.0.1:8000 (PID 15554).`
- `.tmp/api.log`
  - Uvicorn startup completed
  - Logged one `GET /health` `200 OK`
- `make status`
  - `API PID not tracked.`
  - `Health: unavailable (http://127.0.0.1:8000/health)`
- direct uvicorn in TTY
  - bind failure: `ERROR: [Errno 1] error while attempting to bind on address ('127.0.0.1', 8000): operation not permitted`
- escalated 8011 curl checks
  - all failed: `curl: (7) Failed to connect to 127.0.0.1 port 8011`
- TestClient probe
  - `GET /health 200 {'status': 'ok'}`
  - `POST /ask answerable 200 answerable 1`
  - `POST /ask insufficient 200 not_enough_evidence 0`
  - `POST /ask long question 422`
  - `POST /run-eval 200 18 18`
  - `POST /run-eval extra field 422`

## What passed
- Repository inventory and documentation scan
- `make lint`
- `make test`
- CLI `index-demo`
- CLI `ask-demo` for support answerable and support unanswerable cases
- CLI `ask-demo` for one academic case
- CLI `run-eval`
- In-process API verification through FastAPI `TestClient`
- Eval report generation and report file inspection

## What failed
- Stable live `curl` verification against background server on `127.0.0.1:8000`
- Stable live `curl` verification against escalated background server on `127.0.0.1:8011`
- Direct uvicorn bind in one TTY session due `operation not permitted`
- `ps` process inspection inside sandbox: `operation not permitted`

## What was not runnable or not verified
- Fresh editable install from scratch via `python -m pip install -e .` was not attempted to avoid mutating the environment
- Browser rendering in a real browser session
- A separate standalone UI server does not exist
- Public-deployment safety was not verified because the repo is explicitly local-only demo software
