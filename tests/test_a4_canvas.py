import pytest
import sys
from unittest.mock import MagicMock

# Mock PIL before importing src modules
mock_pil = MagicMock()
sys.modules["PIL"] = mock_pil
sys.modules["PIL.Image"] = mock_pil.Image

from src.layout.a4_canvas import SafeZoneBoundary, A4Canvas, A4_LANDSCAPE_PX_300DPI, MM_TO_PX_300DPI

def test_safe_zone_boundary_contains():
    # Safe zone: (10, 10) to (100, 100)
    sz = SafeZoneBoundary(x_min_px=10, y_min_px=10, x_max_px=100, y_max_px=100)

    # Point inside
    assert sz.contains(20, 20) is True
    # Point outside
    assert sz.contains(5, 20) is False
    assert sz.contains(20, 5) is False
    assert sz.contains(105, 20) is False
    assert sz.contains(20, 105) is False

    # Rectangle inside
    assert sz.contains(20, 20, 50, 50) is True
    # Rectangle partially outside
    assert sz.contains(80, 80, 30, 30) is False
    # Rectangle exactly on boundary
    assert sz.contains(10, 10, 90, 90) is True

def test_a4_canvas_initialization_default():
    canvas = A4Canvas()
    assert canvas.width == A4_LANDSCAPE_PX_300DPI[0]
    assert canvas.height == A4_LANDSCAPE_PX_300DPI[1]

    # Verify safe zone calculation
    # "safe_zone": {"x_pct": 0.00, "y_pct": 0.00, "w_pct": 0.505, "h_pct": 0.714}
    assert canvas.safe_zone.x_min_px == 0
    assert canvas.safe_zone.y_min_px == 0
    assert canvas.safe_zone.x_max_px == int(3508 * 0.505)
    assert canvas.safe_zone.y_max_px == int(2480 * 0.714)

def test_a4_canvas_initialization_custom():
    canvas = A4Canvas(target_width=1000, target_height=707) # ~A4 aspect ratio
    assert canvas.width == 1000
    assert canvas.height == 707
    assert canvas.safe_zone.x_max_px == int(1000 * 0.505)
    assert canvas.safe_zone.y_max_px == int(707 * 0.714)

def test_mm_to_px_conversion():
    canvas = A4Canvas()
    # 25.4 mm = 1 inch = 300 px at 300 DPI
    assert canvas.mm_to_px(25.4) == 300
    assert canvas.mm_to_px(0) == 0

def test_px_to_mm_conversion():
    canvas = A4Canvas()
    assert canvas.px_to_mm(300) == 25.4
    assert canvas.px_to_mm(0) == 0.0

def test_get_element_rect():
    canvas = A4Canvas()

    # "title_scroll": {"x_pct": 0.02, "y_pct": 0.02, "w_pct": 0.22, "h_pct": 0.10}
    rect = canvas.get_element_rect("title_scroll")
    assert rect["x"] == int(3508 * 0.02)
    assert rect["y"] == int(2480 * 0.02)
    assert rect["w"] == int(3508 * 0.22)
    assert rect["h"] == int(2480 * 0.10)

    # Test invalid element
    with pytest.raises(ValueError, match="Unknown element"):
        canvas.get_element_rect("non_existent_element")

def test_get_bento_card_rects():
    canvas = A4Canvas()

    # Test with 3 cards (default)
    cards = canvas.get_bento_card_rects(3)
    assert len(cards) == 3

    # Verify card 1 position and dimensions
    # Bento grid: {"x_pct": 0.02, "y_pct": 0.14, "w_pct": 0.46, "h_pct": 0.55}
    bento = canvas.get_element_rect("bento_grid")
    card_gap = int(bento["w"] * 0.02)
    card_w = (bento["w"] - 2 * card_gap) // 3

    assert cards[0]["x"] == bento["x"]
    assert cards[0]["w"] == card_w
    assert cards[1]["x"] == bento["x"] + card_w + card_gap

    # Test with max 3 cards constraint
    cards_more = canvas.get_bento_card_rects(5)
    assert len(cards_more) == 3

def test_validate_safe_zone():
    canvas = A4Canvas()

    # Element inside
    elements_inside = [{"x": 10, "y": 10, "w": 50, "h": 50}]
    valid, violations = canvas.validate_safe_zone(elements_inside)
    assert valid is True
    assert len(violations) == 0

    # Element outside
    elements_outside = [{"x": 3000, "y": 2000, "w": 1000, "h": 1000}]
    valid, violations = canvas.validate_safe_zone(elements_outside)
    assert valid is False
    assert len(violations) == 1
    assert violations[0]["element_index"] == 0

def test_get_layout_manifest():
    canvas = A4Canvas()
    manifest = canvas.get_layout_manifest()

    assert "canvas" in manifest
    assert "safe_zone" in manifest
    assert "zones" in manifest
    assert "elements" in manifest

    assert manifest["canvas"]["width"] == 3508
    assert manifest["elements"]["title_scroll"] == canvas.get_element_rect("title_scroll")

def test_normalize_background():
    # Mocking PIL.Image.open and resize
    mock_image = MagicMock()
    mock_pil.Image.open.return_value = mock_image
    mock_image.convert.return_value = mock_image
    mock_image.size = (100, 100)

    A4Canvas.normalize_background("dummy.png")

    mock_pil.Image.open.assert_called_with("dummy.png")
    mock_image.resize.assert_called()
