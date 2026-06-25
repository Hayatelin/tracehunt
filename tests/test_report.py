"""Offline tests for the TraceHunt report module (no network, no heavy deps)."""
import os
from tracehunt.result import QueryResult, QueryStatus
from tracehunt import report


def _fake_results(found=3, missing=2):
    results = {}
    for i in range(found):
        site = f"FoundSite{i}"
        results[site] = {"url_main": f"https://{site}.com", "url_user": f"https://{site}.com/user",
                         "http_status": 200,
                         "status": QueryResult("user", site, f"https://{site}.com/user", QueryStatus.CLAIMED, query_time=0.5)}
    for i in range(missing):
        site = f"MissingSite{i}"
        results[site] = {"url_main": f"https://{site}.com", "url_user": f"https://{site}.com/user",
                         "http_status": 404,
                         "status": QueryResult("user", site, f"https://{site}.com/user", QueryStatus.AVAILABLE, query_time=0.3)}
    return results


def test_summarize_counts():
    s = report.summarize("user", _fake_results(3, 2))
    assert s["checked"] == 5 and s["found"] == 3 and s["avg_response_time_s"] == 0.5


def test_score_zero_when_no_hits():
    assert report.summarize("user", _fake_results(0, 4))["footprint_score"] == 0


def test_score_increases_with_hits():
    low = report.summarize("u", _fake_results(1, 0))["footprint_score"]
    high = report.summarize("u", _fake_results(10, 0))["footprint_score"]
    assert 0 < low < high <= 100


def test_write_html(tmp_path):
    out = tmp_path / "report.html"
    report.write_html("johndoe", _fake_results(2, 3), str(out))
    html = out.read_text(encoding="utf-8")
    assert os.path.isfile(out) and "johndoe" in html and "FOUND" in html and "Footprint score" in html


def test_print_summary_runs(capsys):
    report.print_summary(report.summarize("user", _fake_results()))
    assert "Digital footprint summary" in capsys.readouterr().out
