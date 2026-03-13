"""Static HTML UI for local demo."""
# ruff: noqa: E501

UI_HTML = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Universal RAG Copilot</title>
  <style>
    :root { --bg:#f4f5f7; --panel:#fff; --line:#d8dbe2; --text:#1f2937; --muted:#596579; --ok:#0f766e; --warn:#b45309; --chip:#e8edf5; }
    body { margin:0; font:14px/1.45 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; background:var(--bg); color:var(--text); }
    main { max-width:980px; margin:24px auto; padding:0 16px; }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:16px; margin-bottom:14px; }
    h1 { margin:0 0 6px; font-size:22px; }
    h2 { margin:0 0 12px; font-size:16px; }
    h3 { margin:0 0 8px; font-size:13px; }
    .row { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }
    .row3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }
    label { display:block; font-size:12px; color:var(--muted); margin-bottom:4px; }
    input,select,button,textarea { width:100%; box-sizing:border-box; padding:8px; border:1px solid var(--line); border-radius:8px; }
    textarea { min-height:84px; resize:vertical; }
    button { cursor:pointer; background:#1f3b67; color:#fff; border:0; }
    button.secondary { background:#475569; }
    pre { background:#0b1020; color:#d7ddf8; padding:10px; border-radius:8px; overflow:auto; }
    .result-grid { display:grid; gap:12px; }
    .answer-box { background:#f8fafc; border:1px solid var(--line); border-radius:8px; padding:12px; }
    .badge { display:inline-block; padding:4px 8px; border-radius:999px; font-size:12px; font-weight:600; background:var(--chip); }
    .badge.answerable { color:var(--ok); }
    .badge.not_enough_evidence { color:var(--warn); }
    .list { margin:0; padding-left:18px; }
    .mono { font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; font-size:12px; }
    .muted { color:var(--muted); }
    @media (max-width: 760px) { .row,.row3 { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <main>
    <div class=\"card\">
      <h1>Universal RAG Copilot</h1>
      <div class=\"muted\">Local-first grounded QA demo with answerability checks</div>
    </div>

    <div class=\"card\">
      <h2>Ask</h2>
      <div class=\"row\">
        <div><label for=\"mode\">Mode</label><select id=\"mode\"><option>support_kb</option><option>academic_pdf</option></select></div>
        <div><label for=\"profile\">Profile</label><select id=\"profile\"><option>fine</option><option selected>balanced</option><option>coarse</option></select></div>
      </div>
      <div style=\"margin-top:10px\"><label for=\"question\">Question</label><textarea id=\"question\">How long do card refunds take to settle?</textarea></div>
      <div class=\"row3\" style=\"margin-top:10px\">
        <div><label for=\"top_k\">Top K</label><input id=\"top_k\" type=\"number\" min=\"1\" value=\"4\" /></div>
        <div><label for=\"min_score_threshold\">Min Score Threshold</label><input id=\"min_score_threshold\" type=\"number\" min=\"0\" step=\"0.01\" value=\"0.07\" /></div>
        <div><label for=\"min_evidence_results\">Min Evidence Results</label><input id=\"min_evidence_results\" type=\"number\" min=\"1\" value=\"1\" /></div>
      </div>
      <div style=\"margin-top:10px\"><button id=\"askBtn\">Ask</button></div>
    </div>

    <div class=\"card\">
      <h2>Answer Result</h2>
      <div id=\"askResult\" class=\"result-grid muted\">No query yet.</div>
    </div>

    <div class=\"card\">
      <h2>Evaluation</h2>
      <button id=\"evalBtn\" class=\"secondary\">Run Local Eval</button>
      <div id=\"evalResult\" class=\"result-grid muted\">No eval run yet.</div>
      <div id=\"latestEvalPath\" class=\"muted\"></div>
    </div>
  </main>

  <script>
    const askResult = document.getElementById('askResult');
    const evalResult = document.getElementById('evalResult');
    const latestEvalPath = document.getElementById('latestEvalPath');

    function escapeHtml(value) {
      return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('\"', '&quot;');
    }

    function renderAskResult(body) {
      const citations = (body.citations || []).map((citation) => `
        <li>
          <strong>${escapeHtml(citation.title)}</strong>
          <span class=\"muted\">${escapeHtml(citation.section || 'section unavailable')}</span>
          <div class=\"mono\">${escapeHtml(citation.chunk_id)} | score ${escapeHtml(citation.score)}</div>
        </li>
      `).join('');
      const topResults = (body.retrieval_summary?.top_results || []).map((item) => `
        <li class=\"mono\">${escapeHtml(item.document_id)} :: ${escapeHtml(item.chunk_id)} :: score ${escapeHtml(item.score)}</li>
      `).join('');

      askResult.className = 'result-grid';
      askResult.innerHTML = `
        <div class=\"answer-box\">
          <h3>Answerability</h3>
          <div class=\"badge ${escapeHtml(body.answerability)}\">${escapeHtml(body.answerability)}</div>
        </div>
        <div class=\"answer-box\">
          <h3>Answer</h3>
          <div>${escapeHtml(body.answer)}</div>
        </div>
        <div class=\"answer-box\">
          <h3>Citations</h3>
          ${citations ? `<ul class=\"list\">${citations}</ul>` : '<div class=\"muted\">No citations returned.</div>'}
        </div>
        <div class=\"answer-box\">
          <h3>Retrieval Summary</h3>
          <div class=\"muted\">eligible ${escapeHtml(body.retrieval_summary?.eligible_count ?? 0)} / retrieved ${escapeHtml(body.retrieval_summary?.retrieved_count ?? 0)}</div>
          ${topResults ? `<ul class=\"list\">${topResults}</ul>` : '<div class=\"muted\">No retrieval hits.</div>'}
        </div>
      `;
    }

    function renderEvalResult(body) {
      evalResult.className = 'result-grid';
      evalResult.innerHTML = `
        <div class=\"answer-box\">
          <h3>Summary</h3>
          <div><strong>${escapeHtml(body.passed_cases)}</strong> / ${escapeHtml(body.total_cases)} cases passed</div>
        </div>
        <div class=\"answer-box\">
          <h3>Reports</h3>
          <div class=\"mono\">JSON: ${escapeHtml(body.json_report_path || 'n/a')}</div>
          <div class=\"mono\">Markdown: ${escapeHtml(body.markdown_report_path || 'n/a')}</div>
        </div>
      `;
    }

    document.getElementById('askBtn').onclick = async () => {
      const payload = {
        mode: document.getElementById('mode').value,
        profile: document.getElementById('profile').value,
        question: document.getElementById('question').value,
        top_k: Number(document.getElementById('top_k').value),
        min_score_threshold: Number(document.getElementById('min_score_threshold').value),
        min_evidence_results: Number(document.getElementById('min_evidence_results').value)
      };
      const res = await fetch('/ask', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
      const body = await res.json();
      if (!res.ok) {
        askResult.className = 'result-grid muted';
        askResult.textContent = JSON.stringify(body, null, 2);
        return;
      }
      renderAskResult(body);
    };

    document.getElementById('evalBtn').onclick = async () => {
      const res = await fetch('/run-eval', { method:'POST', headers:{'Content-Type':'application/json'}, body:'{}' });
      const body = await res.json();
      if (!res.ok) {
        evalResult.className = 'result-grid muted';
        evalResult.textContent = JSON.stringify(body, null, 2);
        return;
      }
      renderEvalResult(body);
      latestEvalPath.textContent = body.json_report_path ? `Latest eval: ${body.json_report_path}` : '';
    };
  </script>
</body>
</html>
"""
