"""Offline tests for the TraceHunt YAML config loader."""
import pytest
from tracehunt.config import load_config
yaml = pytest.importorskip("yaml")


def test_missing_file_returns_empty(tmp_path):
    assert load_config(str(tmp_path / "nope.yaml")) == {}


def test_loads_allowed_keys_only(tmp_path):
    cfg = tmp_path / "tracehunt.yaml"
    cfg.write_text("timeout: 30\nsummary: true\nbogus_key: 123\n", encoding="utf-8")
    assert load_config(str(cfg)) == {"timeout": 30, "summary": True}


def test_non_dict_returns_empty(tmp_path):
    cfg = tmp_path / "tracehunt.yaml"
    cfg.write_text("- a\n- b\n", encoding="utf-8")
    assert load_config(str(cfg)) == {}
