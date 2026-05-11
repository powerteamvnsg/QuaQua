
import os
import json
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, Any

class LayoutEngine:
    """
    Deterministic Image Compositor.
    Renamed 'assemble' to match main_factory.py expectations.
    """
    CANVAS_WIDTH = 3508
    CANVAS_HEIGHT = 2480
    
    def __init__(self, schema_path: Path, output_dir: Path):
        self.schema_path = schema_path
        self.output_dir = output_dir
        self.schema = self._load_json(self.schema_path)
        
        # Load themes just for the fixed component paths (logic from previous version)
        themes_path = Path(r"d:\AntiGravity Projects\k2-worksheet-generator\config\overlay_themes.json")
        self.themes = self._load_json(themes_path) if themes_path.exists() else {}

    def _load_json(self, path: Path) -> Dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _auto_trim(self, image: Image.Image) -> Image.Image:
        """Strips pure backgrounds and crops to content."""
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        data = np.array(image)
        # Check corners for background color
        corners = [data[0,0,:3], data[0,-1,:3], data[-1,0,:3], data[-1,-1,:3]]
        unique, counts = np.unique(corners, axis=0, return_counts=True)
        bg_color = unique[np.argmax(counts)]

        # If it's a light background (white/grey), make it transparent
        if bg_color[0] > 230 and bg_color[1] > 230 and bg_color[2] > 230:
            mask = (data[:,:,0] > 230) & (data[:,:,1] > 230) & (data[:,:,2] > 230)
            data[mask, 3] = 0
        
        trimmed = Image.fromarray(data)
        bbox = trimmed.getbbox()
        return trimmed.crop(bbox) if bbox else trimmed

    def assemble(self, theme_name: str, assets: Dict[str, str], layout_config: Dict[str, Any] = None) -> str:
        """
        Takes validated asset paths and a layout schema to build the final worksheet frame.
        Assets dict: {'banner': path, 'scene': path, 'mascot': path, 'bottom': path, 'right': path}
        """
        canvas = Image.new("RGBA", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))
        zones = self.schema.get("overlay_zones", {})
        
        print(f"\n🧩 [Assembly] Stacking layers for {theme_name}...")
        
        # Mapping asset types to zone names in the schema
        layer_mapping = [
            ("bottom_frame_strip", assets.get("bottom")),
            ("right_frame_strip", assets.get("right")),
            ("character_scene", assets.get("scene")),
            ("title_banner_frame", assets.get("banner")),
            # Mascot path is handled as part of the scene or overlay depending on schema
        ]
        
        for zone_name, path in layer_mapping:
            if not path or not os.path.exists(path):
                continue
                
            zone = zones.get(zone_name, {})
            w, h = zone.get("width", 500), zone.get("height", 500)
            x, y = zone.get("x", 0), zone.get("y", 0)
            
            img = Image.open(path).convert("RGBA")
            img = self._auto_trim(img)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            
            canvas.paste(img, (x, y), img)
            print(f"   ✓ Layered {zone_name}")

        # Final production save
        output_filename = f"{theme_name}_worksheet_frame.png"
        output_path = self.output_dir / "production" / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        canvas.save(output_path, "PNG")
        return str(output_path)
