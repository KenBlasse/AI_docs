"""Tests für scripts/validate_newsletter.py — HTML-Wohlgeformtheit + Härtung (#4)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_newsletter as vn  # noqa: E402


def test_rendered_template_is_valid():
    """Das mitgelieferte, gehärtete Template muss durchlaufen."""
    assert vn.validate_html(vn.render_template()) == []


def test_script_is_rejected():
    html = "<html><head><title>T</title></head><body><div style='max-width:600px'><script>x</script></div></body></html>"
    errors = vn.validate_html(html)
    assert any("script" in e.lower() for e in errors)


def test_img_without_alt_is_rejected():
    html = "<html><head><title>T</title></head><body><div style='max-width:600px'><img src='a.png'></div></body></html>"
    assert any("alt" in e for e in vn.validate_html(html))


def test_img_with_alt_passes():
    html = "<html><head><title>T</title></head><body><div style='max-width:600px'><img src='a.png' alt='Bild'></div></body></html>"
    assert not any("alt" in e for e in vn.validate_html(html))


def test_missing_title_is_rejected():
    html = "<html><head><title></title></head><body><div style='max-width:600px'>x</div></body></html>"
    assert any("title" in e.lower() for e in vn.validate_html(html))


def test_unbalanced_tags_are_rejected():
    html = "<html><head><title>T</title></head><body><div style='max-width:600px'><p>offen</div></body></html>"
    errors = vn.validate_html(html)
    assert any("unbalanc" in e.lower() or "erwartet" in e.lower() for e in errors)


def test_missing_max_width_is_rejected():
    html = "<html><head><title>T</title></head><body><p>kein container</p></body></html>"
    assert any("max-width" in e for e in vn.validate_html(html))


def test_style_in_head_is_rejected():
    html = "<html><head><title>T</title><style>p{color:red}</style></head><body><div style='max-width:600px'>x</div></body></html>"
    assert any("<style>" in e for e in vn.validate_html(html))


def test_void_elements_dont_break_balance():
    """br/img/meta etc. brauchen kein End-Tag — dürfen Balance nicht stören."""
    html = "<html><head><title>T</title></head><body><div style='max-width:600px'><br><hr>ok</div></body></html>"
    errors = vn.validate_html(html)
    assert not any("schlossen" in e.lower() or "unbalanc" in e.lower() for e in errors)
