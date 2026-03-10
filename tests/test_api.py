from fastapi.testclient import TestClient

from universal_rag_copilot.api.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_redirects_to_ui() -> None:
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/ui"


def test_ui_returns_html() -> None:
    response = client.get("/ui")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Universal RAG Copilot" in response.text


def test_ui_head_returns_200_html_no_body() -> None:
    response = client.head("/ui")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert response.text == ""


def test_ask_happy_path() -> None:
    response = client.post(
        "/ask",
        json={
            "mode": "support_kb",
            "profile": "balanced",
            "question": "How long do card refunds take to settle?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answerability"] == "answerable"
    assert body["answer"]
    assert body["citations"]
    assert set(body["retrieval_summary"]) == {
        "top_k",
        "min_score_threshold",
        "min_evidence_results",
        "retrieved_count",
        "eligible_count",
        "top_results",
    }


def test_ask_insufficient_evidence_case() -> None:
    response = client.post(
        "/ask",
        json={
            "mode": "support_kb",
            "profile": "balanced",
            "question": "How do I renew a passport in Canada?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["answerability"] == "not_enough_evidence"
    assert "Not enough evidence" in body["answer"]
    assert body["citations"] == []


def test_run_eval_response_shape(tmp_path) -> None:
    response = client.post("/run-eval", json={"output_dir": str(tmp_path)})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "total_cases",
        "passed_cases",
        "json_report_path",
        "markdown_report_path",
    }
    assert body["total_cases"] >= 3
    assert body["passed_cases"] <= body["total_cases"]
