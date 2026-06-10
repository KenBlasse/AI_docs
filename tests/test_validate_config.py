"""Tests für scripts/validate_config.py — Meta-Schema für Config (#7)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_config as vc  # noqa: E402


def test_real_config_is_valid():
    """Die ausgelieferte Config muss konsistent sein."""
    assert vc.validate() == []


def test_config_schema_catches_missing_extension():
    bad = {"output_dir": "x", "global_rules": "g", "schema": "s",
           "types": {"foo": {"rules": "r", "template": "t"}}}  # extension fehlt
    errors = vc._schema_errors(bad, vc.CONFIG_SCHEMA, "config.yaml")
    assert any("extension" in e for e in errors)


def test_config_schema_catches_typo_key():
    bad = {"output_dir": "x", "global_rules": "g", "schema": "s",
           "typ": {}}  # 'typ' statt 'types' → additionalProperties + required
    errors = vc._schema_errors(bad, vc.CONFIG_SCHEMA, "config.yaml")
    assert errors


def test_frontmatter_meta_catches_non_object_type():
    bad = {"types": {"foo": {"type": "string", "properties": {"x": {}}}}}
    errors = vc._schema_errors(bad, vc.FRONTMATTER_META, "frontmatter.yaml")
    assert any("const" in e or "object" in e for e in errors)


def test_frontmatter_meta_requires_properties():
    bad = {"types": {"foo": {"type": "object"}}}  # properties fehlt
    errors = vc._schema_errors(bad, vc.FRONTMATTER_META, "frontmatter.yaml")
    assert any("properties" in e for e in errors)


def test_cross_check_detects_orphan_schema(tmp_path, monkeypatch):
    """Ein Schema-Typ ohne config-Eintrag wird als verwaist gemeldet."""
    cfg = tmp_path / "config.yaml"
    fm = tmp_path / "frontmatter.yaml"
    (tmp_path / "r.md").write_text("x")
    (tmp_path / "t.md").write_text("x")
    (tmp_path / "g.md").write_text("x")
    cfg.write_text(
        "output_dir: ./out\nglobal_rules: g.md\nschema: frontmatter.yaml\n"
        "types:\n  foo:\n    rules: r.md\n    template: t.md\n    extension: md\n"
    )
    fm.write_text(
        "types:\n"
        "  foo: {type: object, properties: {title: {type: string}}}\n"
        "  verwaist: {type: object, properties: {title: {type: string}}}\n"
    )
    monkeypatch.setattr(vc, "ROOT", tmp_path)
    monkeypatch.setattr(vc, "CONFIG_PATH", cfg)
    monkeypatch.setattr(vc, "SCHEMA_PATH", fm)
    problems = vc.validate()
    assert any("verwaist" in p for p in problems)
