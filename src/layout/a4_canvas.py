"""
Phase 1: A4 Canvas Dimensional Standardization
Provides normalized A4 Landscape coordinates with percentage-based anchoring.

A4 Landscape: 297mm × 210mm (aspect ratio 1.414:1)
At 300 DPI: 3508 × 2480 pixels
"""

from dataclasses import dataclass
from typing import Tuple, Dict
from PIL import Image

# === A4 CONSTANTS ===
A4_LANDSCAPE_MM = (297, 210)
A4_LANDSCAPE_PX_300DPI = (3508, 2480)
A4_ASPECT_RATIO = 297 / 210  # 1.414

# DPI conversion factor
MM_TO_PX_300DPI = 300 / 25.4  # ~11.811 px per mm


@dataclass
class SafeZoneBoundary:
    """
    Defines the academic content boundary.
    All teaching elements must fit within this zone.
    """
    x_min_px: int
    y_min_px: int
    x_max_px: int
    y_max_px: int
    
    def contains(self, x: int, y: int, w: int = 0, h: int = 0) -> bool:
        """Check if a bounding box fits entirely within the safe zone."""
        return (x >= self.x_min_px and 
                y >= self.y_min_px and 
                x + w <= self.x_max_px and 
                y + h <= self.y_max_px)
    
    def to_dict(self) -> dict:
        return {
            "x_min": self.x_min_px,
            "y_min": self.y_min_px,
            "x_max": self.x_max_px,
            "y_max": self.y_max_px
        }


class A4Canvas:
    """
    A4 Landscape Canvas Manager.
    
    Responsibilities:
    - Normalize any input image to A4 aspect ratio using Lanczos resampling
    - Calculate percentage-based coordinates
    - Enforce Safe Zone boundaries
    - Convert between mm and pixels
    
    CONTRACT:
    - All coordinates returned are in pixels at 300 DPI
    - Safe Zone is strictly enforced (150mm × 150mm top-left)
    - Background images are resampled to exact A4 dimensions
    """
    
    # === ZONE DEFINITIONS (Percentage-Based) ===
    ZONES = {
        # Academic Safe Zone: Top-left 150mm × 150mm
        # At 297mm width: 150mm = 50.5% of width
        # At 210mm height: 150mm = 71.4% of height
        "safe_zone": {
            "x_pct": 0.00,
            "y_pct": 0.00,
            "w_pct": 0.505,  # 150mm / 297mm
            "h_pct": 0.714   # 150mm / 210mm
        },
        # Grass Zone: Bottom 12% (forbidden for academic content)
        "grass_zone": {
            "y_start_pct": 0.88,  # Starts at 88% from top
            "h_pct": 0.12
        },
        # Map Zone: Right 40% (reserved for adventure path drawing)
        "map_zone": {
            "x_start_pct": 0.60,  # Starts at 60% from left
            "w_pct": 0.40
        }
    }
    
    # === ELEMENT POSITIONS (Percentage-Based, WITHIN 150mm Safe Zone) ===
    # Safe Zone: 150mm × 150mm = 50.5% × 71.4% of A4
    # All elements must fit within X:[0, 0.505] and Y:[0, 0.714]
    ELEMENTS = {
        "title_scroll": {
            "x_pct": 0.02,   # 2% from left
            "y_pct": 0.02,   # 2% from top
            "w_pct": 0.22,   # 22% of canvas width (within 50.5%)
            "h_pct": 0.10    # 10% of canvas height
        },
        "instruction_box": {
            "x_pct": 0.26,   # 26% from left (adjacent to title)
            "y_pct": 0.02,   # 2% from top
            "w_pct": 0.22,   # 22% of canvas width (26% + 22% = 48% < 50.5%)
            "h_pct": 0.08    # 8% of canvas height
        },
        "bento_grid": {
            "x_pct": 0.02,   # 2% from left
            "y_pct": 0.14,   # 14% from top (below title/instructions)
            "w_pct": 0.46,   # 46% of canvas width (within 50.5% safe zone)
            "h_pct": 0.55    # 55% of canvas height (14% + 55% = 69% < 71.4%)
        }
    }
    
    def __init__(self, target_width: int = None, target_height: int = None):
        """
        Initialize canvas with target dimensions.
        Defaults to 300 DPI A4 Landscape if not specified.
        """
        if target_width and target_height:
            # Validate aspect ratio
            ratio = target_width / target_height
            if abs(ratio - A4_ASPECT_RATIO) > 0.01:
                print(f"⚠️ Non-A4 aspect ratio detected ({ratio:.3f}). Will normalize.")
            self.width = target_width
            self.height = target_height
        else:
            self.width, self.height = A4_LANDSCAPE_PX_300DPI
        
        # Calculate Safe Zone boundary in pixels
        self._calculate_safe_zone()
    
    def _calculate_safe_zone(self):
        """Calculate the 150mm × 150mm safe zone in pixels."""
        sz = self.ZONES["safe_zone"]
        self.safe_zone = SafeZoneBoundary(
            x_min_px=int(self.width * sz["x_pct"]),
            y_min_px=int(self.height * sz["y_pct"]),
            x_max_px=int(self.width * sz["w_pct"]),
            y_max_px=int(self.height * sz["h_pct"])
        )
    
    @staticmethod
    def normalize_background(image_path: str, output_path: str = None) -> Image.Image:
        """
        Normalize any background image to A4 Landscape using Lanczos resampling.
        
        Args:
            image_path: Path to source image
            output_path: Optional path to save normalized image
            
        Returns:
            PIL Image object at A4 dimensions (3508 × 2480)
        """
        img = Image.open(image_path).convert("RGBA")
        original_size = img.size
        
        target_w, target_h = A4_LANDSCAPE_PX_300DPI
        
        if img.size != (target_w, target_h):
            print(f"📐 Normalizing background: {original_size} → ({target_w}, {target_h})")
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        if output_path:
            img.save(output_path)
            print(f"✅ Saved normalized background to: {output_path}")
        
        return img
    
    def get_element_rect(self, element_name: str) -> Dict[str, int]:
        """
        Get pixel coordinates for a named element using percentage-based anchoring.
        
        Args:
            element_name: One of 'title_scroll', 'instruction_box', 'bento_grid'
            
        Returns:
            Dict with x, y, w, h in pixels
        """
        if element_name not in self.ELEMENTS:
            raise ValueError(f"Unknown element: {element_name}. Valid: {list(self.ELEMENTS.keys())}")
        
        elem = self.ELEMENTS[element_name]
        rect = {
            "x": int(self.width * elem["x_pct"]),
            "y": int(self.height * elem["y_pct"]),
            "w": int(self.width * elem["w_pct"]),
            "h": int(self.height * elem["h_pct"])
        }
        
        # Validate against safe zone
        if not self.safe_zone.contains(rect["x"], rect["y"], rect["w"], rect["h"]):
            print(f"⚠️ WARNING: '{element_name}' exceeds safe zone boundary!")
        
        return rect
    
    def get_bento_card_rects(self, num_cards: int = 3) -> list:
        """
        Calculate positions for Bento cards within the work area.
        Cards are arranged horizontally with equal spacing.
        
        Args:
            num_cards: Number of cards to arrange (max 3)
            
        Returns:
            List of dicts with x, y, w, h for each card
        """
        num_cards = min(num_cards, 3)  # Enforce max
        
        bento = self.get_element_rect("bento_grid")
        
        # Calculate card dimensions
        card_gap = int(bento["w"] * 0.02)  # 2% gap between cards
        total_gap = card_gap * (num_cards - 1)
        card_w = (bento["w"] - total_gap) // num_cards
        card_h = int(bento["h"] * 0.95)  # 95% of available height
        
        cards = []
        for i in range(num_cards):
            card = {
                "id": f"card_{i+1}",
                "x": bento["x"] + (i * (card_w + card_gap)),
                "y": bento["y"],
                "w": card_w,
                "h": card_h
            }
            
            # Validate each card is within safe zone
            if not self.safe_zone.contains(card["x"], card["y"], card["w"], card["h"]):
                print(f"⚠️ WARNING: Card {i+1} exceeds safe zone! Clamping...")
                card["x"] = min(card["x"], self.safe_zone.x_max_px - card["w"])
                card["w"] = min(card["w"], self.safe_zone.x_max_px - card["x"])
                card["h"] = min(card["h"], self.safe_zone.y_max_px - card["y"])
            
            cards.append(card)
        
        return cards
    
    def mm_to_px(self, mm: float) -> int:
        """Convert millimeters to pixels at 300 DPI."""
        return int(mm * MM_TO_PX_300DPI)
    
    def px_to_mm(self, px: int) -> float:
        """Convert pixels to millimeters at 300 DPI."""
        return px / MM_TO_PX_300DPI
    
    def validate_safe_zone(self, elements: list) -> Tuple[bool, list]:
        """
        Validate that all elements fit within the safe zone.
        
        Args:
            elements: List of dicts with x, y, w, h keys
            
        Returns:
            Tuple of (all_valid, list of violations)
        """
        violations = []
        
        for i, elem in enumerate(elements):
            if not self.safe_zone.contains(elem["x"], elem["y"], 
                                           elem.get("w", 0), elem.get("h", 0)):
                violations.append({
                    "element_index": i,
                    "element": elem,
                    "safe_zone": self.safe_zone.to_dict(),
                    "message": f"Element {i} exceeds safe zone boundary"
                })
        
        return len(violations) == 0, violations
    
    def get_layout_manifest(self) -> dict:
        """
        Generate a complete layout manifest with all calculated positions.
        """
        return {
            "canvas": {
                "width": self.width,
                "height": self.height,
                "aspect_ratio": round(self.width / self.height, 3),
                "dpi": 300,
                "format": "A4_LANDSCAPE"
            },
            "safe_zone": self.safe_zone.to_dict(),
            "zones": {
                "grass_zone": {
                    "y_start": int(self.height * self.ZONES["grass_zone"]["y_start_pct"]),
                    "height": int(self.height * self.ZONES["grass_zone"]["h_pct"]),
                    "note": "FORBIDDEN for academic content"
                },
                "map_zone": {
                    "x_start": int(self.width * self.ZONES["map_zone"]["x_start_pct"]),
                    "width": int(self.width * self.ZONES["map_zone"]["w_pct"]),
                    "note": "Reserved for adventure path drawing"
                }
            },
            "elements": {
                "title_scroll": self.get_element_rect("title_scroll"),
                "instruction_box": self.get_element_rect("instruction_box"),
                "bento_grid": self.get_element_rect("bento_grid"),
                "bento_cards": self.get_bento_card_rects(3)
            }
        }


# === UTILITY FUNCTIONS ===

def create_a4_canvas() -> A4Canvas:
    """Factory function to create a standard A4 canvas."""
    return A4Canvas()


def validate_aspect_ratio(width: int, height: int) -> bool:
    """Check if dimensions match A4 aspect ratio (within tolerance)."""
    ratio = width / height
    return abs(ratio - A4_ASPECT_RATIO) < 0.01


if __name__ == "__main__":
    # Test the canvas
    canvas = A4Canvas()
    manifest = canvas.get_layout_manifest()
    
    import json
    print(json.dumps(manifest, indent=2))
