"""
K2 Worksheet Overlay Generator v2.0

Generates themed worksheet overlays with Kawaii-style fruit/vegetable mascots.
Uses CENTER-ORIGIN coordinate system as per layout schematics.

Canvas: 3508x2480px transparent PNG
Center: (1754, 1240)

Components:
  1. Title Banner Frame (top-left) - theme-specific
  2. Instruction Box (top-right) - fixed
  3. Portrait (attached to instruction box) - fixed
  4. Character Scene (bottom-right corner) - theme-specific
  5. Bottom Frame Strip - theme-specific (extends from scene)
  6. Right Frame Strip - theme-specific (extends from scene)

CLI:
    python overlay_generator_v2.py --theme space_mission --list-zones
    python overlay_generator_v2.py --theme space_mission --compose
"""

import os
import json
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from src.config import (
    PROJECT_ROOT, DATA_DIR, ASSETS_DIR, OVERLAY_THEMES_PATH,
    OVERLAY_SCHEMA_PATH, A4_WIDTH, A4_HEIGHT
)

# ============================================================
# CONFIGURATION
# ============================================================

COMPONENTS_DIR = ASSETS_DIR / "overlay_components"
OVERLAYS_DIR = ASSETS_DIR / "overlays"

# Canvas dimensions (A4 Landscape at 300 DPI)
CANVAS_WIDTH = A4_WIDTH
CANVAS_HEIGHT = A4_HEIGHT
CANVAS_CENTER = (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)  # (1754, 1240)


# ============================================================
# COORDINATE UTILITIES
# ============================================================

def center_to_topleft(center_x: int, center_y: int, width: int, height: int) -> Tuple[int, int]:
    """
    Convert center-origin coordinates to top-left origin.
    
    Args:
        center_x: X offset from canvas center
        center_y: Y offset from canvas center
        width: Width of the element
        height: Height of the element
        
    Returns:
        (x, y) tuple for top-left corner in PIL coordinates
    """
    # Convert center offset to absolute canvas position
    abs_center_x = CANVAS_CENTER[0] + center_x
    abs_center_y = CANVAS_CENTER[1] + center_y
    
    # Calculate top-left from center
    top_left_x = abs_center_x - (width // 2)
    top_left_y = abs_center_y - (height // 2)
    
    return (int(top_left_x), int(top_left_y))


def get_zone_bounds(zone_config: Dict) -> Tuple[int, int, int, int]:
    """
    Get PIL-compatible bounds (x, y, width, height) from zone config.
    """
    center = zone_config.get("center", {"x": 0, "y": 0})
    size = zone_config.get("size", {"width": 100, "height": 100})
    
    x, y = center_to_topleft(center["x"], center["y"], size["width"], size["height"])
    return (x, y, size["width"], size["height"])


# ============================================================
# OVERLAY GENERATOR v2
# ============================================================

class OverlayGeneratorV2:
    """
    Generates themed worksheet overlays using center-origin coordinates.
    
    Frame structure:
    - Character Scene (corner focal point)
    - Bottom Strip (extends left from scene)
    - Right Strip (extends up from scene)
    """
    
    def __init__(self, themes_path: Optional[str] = None, layout_path: Optional[str] = None):
        """Initialize with theme and layout configurations."""
        self.themes_path = Path(themes_path) if themes_path else THEMES_PATH
        self.layout_path = Path(layout_path) if layout_path else LAYOUT_SCHEMA_PATH
        
        self.themes = self._load_json(self.themes_path)
        self.layout = self._load_json(self.layout_path)
        self.fixed_components = self._load_fixed_components()
        
    def _load_json(self, path: Path) -> Dict:
        """Load JSON configuration file."""
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _load_fixed_components(self) -> Dict[str, Any]:
        """Load fixed overlay components."""
        components = {}
        for name, info in self.themes.get("fixed_components", {}).items():
            path = PROJECT_ROOT / info["path"]
            if path.exists():
                components[name] = {
                    "image": Image.open(path).convert("RGBA"),
                    "position": (info["position"]["x"], info["position"]["y"])
                }
                print(f"✓ Loaded: {name}")
        return components
    
    def get_zone_positions(self) -> Dict[str, Dict]:
        """Calculate top-left positions for all overlay zones."""
        zones = self.layout.get("overlay_zones", {})
        positions = {}
        
        for zone_name, zone_config in zones.items():
            if zone_name == "frame_zones":
                # Handle nested frame zones
                frame_zones = zone_config
                for fz_name, fz_config in frame_zones.items():
                    if fz_name == "description":
                        continue
                    if "center" in fz_config and "size" in fz_config:
                        x, y, w, h = get_zone_bounds(fz_config)
                        positions[f"frame_{fz_name}"] = {
                            "top_left": (x, y),
                            "size": (w, h),
                            "description": fz_config.get("description", "")
                        }
            elif "center" in zone_config or "frame" in zone_config or "box" in zone_config:
                # Handle single zones with various structures
                if "frame" in zone_config:
                    x, y, w, h = get_zone_bounds(zone_config["frame"])
                    positions[f"{zone_name}_frame"] = {"top_left": (x, y), "size": (w, h)}
                if "box" in zone_config:
                    x, y, w, h = get_zone_bounds(zone_config["box"])
                    positions[f"{zone_name}_box"] = {"top_left": (x, y), "size": (w, h)}
                if "center" in zone_config:
                    # Circular element (portrait)
                    d = zone_config.get("diameter", 100)
                    x, y = center_to_topleft(
                        zone_config["center"]["x"],
                        zone_config["center"]["y"],
                        d, d
                    )
                    positions[zone_name] = {"top_left": (x, y), "size": (d, d)}
        
        return positions
    
    def create_blank_canvas(self) -> Image.Image:
        """Create transparent canvas."""
        return Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    
    def _auto_trim_transparency(self, image: Image.Image) -> Image.Image:
        """
        Strips solid backgrounds (like white) and crops to content.
        """
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        import numpy as np
        data = np.array(image)
        r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

        # Identify the most common color near the corners (likely background)
        corners = [data[0,0,:3], data[0,-1,:3], data[-1,0,:3], data[-1,-1,:3]]
        unique, counts = np.unique(corners, axis=0, return_counts=True)
        bg_color = unique[np.argmax(counts)]

        # Tolerance for background color matching
        tol = 15
        mask = (np.abs(r.astype(int) - bg_color[0]) < tol) & \
               (np.abs(g.astype(int) - bg_color[1]) < tol) & \
               (np.abs(b.astype(int) - bg_color[2]) < tol)
        
        # If the background is very neutral (white/grey), apply transparency
        is_neutral = (np.abs(bg_color[0] - bg_color[1]) < 10) & (np.abs(bg_color[1] - bg_color[2]) < 10)
        if is_neutral and bg_color[0] > 200:
            data[mask, 3] = 0
        
        cleaned_image = Image.fromarray(data)
        bbox = cleaned_image.getbbox()
        if bbox:
            return cleaned_image.crop(bbox)
        return cleaned_image

    def compose_overlay_v2(
        self,
        title_banner_path: Optional[str] = None,
        character_scene_path: Optional[str] = None,
        bottom_frame_path: Optional[str] = None,
        right_frame_path: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Compose overlay with fixed layering and SmartCrop.
        
        Z-ORDER (Back to Front):
          1. Bottom Frame Strip
          2. Right Frame Strip
          3. Character Scene
          4. Title Banner
          5. Instruction Box & Portrait (FRONTmost)
        """
        canvas = self.create_blank_canvas()
        zones = self.layout.get("overlay_zones", {})
        
        print("\n" + "="*60)
        print("COMPOSING OVERLAY v2.2 (Refined Layering & SmartCrop)")
        print("="*60)
        
        # --- PREPARATION: Processing Layers ---
        layers = [
            ("bottom_frame_strip", bottom_frame_path),
            ("right_frame_strip", right_frame_path),
            ("character_scene", character_scene_path),
            ("title_banner_frame", title_banner_path)
        ]

        # Process theme-specific layers first
        for zone_name, path in layers:
            if path and Path(path).exists():
                zone = zones.get(zone_name, {})
                x, y = zone.get("x", 0), zone.get("y", 0)
                w, h = zone.get("width", 100), zone.get("height", 100)
                
                img = Image.open(path).convert("RGBA")
                
                # CRITICAL: Trim before resize to prevent squishing
                img = self._auto_trim_transparency(img)
                
                # Resize to target zone dimensions
                img = img.resize((w, h), Image.Resampling.LANCZOS)
                canvas.paste(img, (x, y), img)
                print(f"✓ Layered: {zone_name} at ({x}, {y}) sized {w}x{h}")

        # ============================================================
        # FRONT LAYER: Fixed Components (Instruction Box + Portrait)
        # ============================================================
        # These are ALWAYS layered last to be on top of frames/scenes
        # We process them specifically from the layout file definitions
        
        # 1. Instruction Box
        ib_zone = zones.get("instruction_box", {})
        fixed_conf = self.themes.get("fixed_components", {}).get("instruction_box", {})
        if fixed_conf:
            img_path = PROJECT_ROOT / fixed_conf["path"]
            if img_path.exists():
                img = Image.open(img_path).convert("RGBA")
                canvas.paste(img, (ib_zone["x"], ib_zone["y"]), img)
                print(f"✓ [Front Layer] Instruction Box at ({ib_zone['x']}, {ib_zone['y']})")

        # 2. Portrait
        p_zone = zones.get("portrait", {})
        # Note: Portrait is usually part of the instruction component or separate
        # If it's a separate file, we layer it here.

        # Save output
        if output_path:
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(output, "PNG")
            print(f"\n✅ COMPLETED: {output.name}")
        
        return canvas
    
    def print_zone_summary(self):
        """Print summary of all zone positions."""
        print("\n" + "="*60)
        print("OVERLAY ZONE POSITIONS (Top-Left Origin)")
        print("="*60)
        
        positions = self.get_zone_positions()
        for name, info in sorted(positions.items()):
            pos = info["top_left"]
            size = info["size"]
            desc = info.get("description", "")
            print(f"\n{name}:")
            print(f"  Position: ({pos[0]}, {pos[1]})")
            print(f"  Size: {size[0]}x{size[1]}")
            if desc:
                print(f"  Note: {desc}")


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="K2 Overlay Generator v2.0")
    parser.add_argument("--list-zones", action="store_true", help="List all zone positions")
    parser.add_argument("--title-banner", type=str, help="Path to title banner image")
    parser.add_argument("--character-scene", type=str, help="Path to character scene image")
    parser.add_argument("--bottom-frame", type=str, help="Path to bottom frame strip")
    parser.add_argument("--right-frame", type=str, help="Path to right frame strip")
    parser.add_argument("--output", type=str, help="Output path")
    
    args = parser.parse_args()
    
    generator = OverlayGeneratorV2()
    
    if args.list_zones:
        generator.print_zone_summary()
        return
    
    if args.output:
        generator.compose_overlay_v2(
            title_banner_path=args.title_banner,
            character_scene_path=args.character_scene,
            bottom_frame_path=args.bottom_frame,
            right_frame_path=args.right_frame,
            output_path=args.output
        )
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
