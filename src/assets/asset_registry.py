"""
Curated Asset Registry - K2 Illustration Style Guide v4.3

Prompt Formulas:
- Animals: Kawaii style [ANIMAL], [VIEW] view, thin black outlines, small dot eyes with tiny white reflection, [COLOR] colors, [POSE], white background, no text
- Objects: Generate Kawaii style objects without faces. [COLOR] [OBJECT], [VIEW] view, thin black outlines, white background, no text
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from src.config import PROJECT_ROOT, DATA_DIR

# === CONFIGURATION ===

# Path to v4.3 kawaii icons (generated with K2_ILLUSTRATION_STYLE_GUIDE.md v4.3)
# TODO: Migrate these icons into the project's data/library/assets/icons/ directory
V43_ICONS_FOLDER = Path(r"C:/Users/tobia/.gemini/antigravity/brain/268cd245-c42d-45b7-8d5d-3a478147acdc")

# Output path for missing assets report
MISSING_ASSETS_PATH = DATA_DIR / "assets" / "missing_assets.json"

# === CURATED ASSET LIBRARY ===
# Generated using K2_ILLUSTRATION_STYLE_GUIDE.md v4.3
# Animals: with faces | Objects: without faces

CURATED_ASSET_LIBRARY: Dict[str, str] = {
    # === V4.3 Animals (with faces) - 2026-01-17 ===
    "cat": str(V43_ICONS_FOLDER / "k2_cat_v42_1768606580981.png"),
    "dog": str(V43_ICONS_FOLDER / "k2_dog_v42_1768606597411.png"),
    "bug": str(V43_ICONS_FOLDER / "k2_bug_v42_1768606611586.png"),
    "sun": str(V43_ICONS_FOLDER / "k2_sun_v42_1768606628534.png"),
    
    # === V4.3 Objects (no faces) - 2026-01-17 ===
    "hat": str(V43_ICONS_FOLDER / "k2_hat_noface_1768607207025.png"),
    "pen": str(V43_ICONS_FOLDER / "k2_pen_noface_1768607221749.png"),
    "log": str(V43_ICONS_FOLDER / "k2_log_noface_1768607235651.png"),
    "pin": str(V43_ICONS_FOLDER / "k2_pin_noface_1768607250069.png"),
    
    # === Pending regeneration with v4.3 style ===
    "run": str(V43_ICONS_FOLDER / "kawaii_run_v4_1768574956534.png"),  # needs regeneration
    "wig": str(V43_ICONS_FOLDER / "kawaii_wig_v4_1768575151153.png"),  # needs regeneration
}

# Icons that still need generation
KNOWN_MISSING = [
    "wig", "run", "hen", "fan", "rat", "jug", "mop", "hug", "pan", "fin", 
    "pot", "can", "net", "bed", "bat", "pig", "cap"
]


class CuratedAssetRegistry:
    """
    Curated Asset Registry - Style-Verified Icons Only.
    
    CRITICAL CHANGE from previous version:
    - NO auto-discovery of random icons
    - Only uses icons from CURATED_ASSET_LIBRARY
    - Logs missing icons for @Illustrator to generate
    
    CONTRACT:
    - resolve() returns path ONLY for verified kawaii icons
    - All icons must match V5.1/V8 Kawaii Style Guide
    - Missing icons are logged to missing_assets.json
    """
    
    _instance = None
    _missing: set = set()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def resolve(self, name: str, quest_id: str = "UNKNOWN") -> Optional[str]:
        """
        Resolve an asset name to its verified file path.
        
        Args:
            name: Asset name (e.g., "cat", "sun")
            quest_id: Quest ID for logging
            
        Returns:
            Path to verified kawaii icon, or None if not in curated library
        """
        clean_name = name.lower().strip()
        
        # Check curated library ONLY
        if clean_name in CURATED_ASSET_LIBRARY:
            path = CURATED_ASSET_LIBRARY[clean_name]
            if os.path.exists(path):
                return path
            else:
                print(f"⚠️ Verified icon file not found: {path}")
                self._log_missing(clean_name, quest_id, "FILE_NOT_FOUND")
                return None
        
        # Not in curated library - log for @Illustrator
        self._log_missing(clean_name, quest_id, "NOT_IN_LIBRARY")
        return None
    
    def _log_missing(self, name: str, quest_id: str, reason: str):
        """Log a missing asset for @Illustrator queue."""
        if name not in self._missing:
            self._missing.add(name)
            print(f"⚠️ MISSING ICON: '{name}' ({reason}) - Needs @Illustrator")
            self._save_missing_report()
    
    def _save_missing_report(self):
        """Save missing assets report for @Illustrator."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "style_guide": "V5.1/V8 Kawaii thin-Line Vector Standard",
            "action_required": "Generate missing icons using @Illustrator agent",
            "missing_icons": sorted(list(self._missing)),
            "prompt_template": (
                "High-quality Kawaii thin-Line Vector Illustration. "
                "Bold thick dark charcoal outlines. Flat cel-shading. "
                "Chibi proportions. Isolated on white background. "
                "Generate: {icon_name}"
            )
        }
        
        MISSING_ASSETS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(MISSING_ASSETS_PATH, "w") as f:
            json.dump(report, f, indent=2)
    
    def get_available_icons(self) -> list:
        """Return list of icons that are verified and available."""
        available = []
        for name, path in CURATED_ASSET_LIBRARY.items():
            if os.path.exists(path):
                available.append(name)
        return available
    
    def get_missing_icons(self) -> list:
        """Return list of icons that need generation."""
        return sorted(list(self._missing))
    
    def has_critical_missing(self) -> bool:
        """Check if there are missing assets."""
        return len(self._missing) > 0
    
    def get_stats(self) -> dict:
        """Return registry statistics."""
        available = self.get_available_icons()
        return {
            "library_size": len(CURATED_ASSET_LIBRARY),
            "available_count": len(available),
            "available_icons": available,
            "missing_count": len(self._missing),
            "missing_icons": self.get_missing_icons()
        }
    
    def clear_missing(self):
        """Clear the missing icons log."""
        self._missing.clear()
        if MISSING_ASSETS_PATH.exists():
            MISSING_ASSETS_PATH.unlink()


# === GLOBAL INSTANCE ===

_registry: Optional[CuratedAssetRegistry] = None


def get_registry() -> CuratedAssetRegistry:
    """Get the global CuratedAssetRegistry instance."""
    global _registry
    if _registry is None:
        _registry = CuratedAssetRegistry()
    return _registry


def resolve_asset(name: str, quest_id: str = "UNKNOWN") -> Optional[str]:
    """Resolve an asset to its verified path."""
    return get_registry().resolve(name, quest_id)


def check_assets_available(names: list, quest_id: str) -> tuple:
    """
    Check if all required icons are available in curated library.
    
    Returns:
        Tuple of (all_available, missing_list)
    """
    registry = get_registry()
    missing = []
    
    for name in names:
        if not registry.resolve(name, quest_id):
            missing.append(name)
    
    return len(missing) == 0, missing


def halt_if_missing(quest_id: str) -> bool:
    """Check if generation should halt due to missing assets."""
    registry = get_registry()
    if registry.has_critical_missing():
        print(f"\n🛑 HALT: Quest {quest_id} cannot proceed.")
        print(f"   Missing icons need @Illustrator generation:")
        for name in registry.get_missing_icons():
            print(f"   - {name}")
        print(f"\n📝 Report saved to: {MISSING_ASSETS_PATH}")
        return True
    return False


if __name__ == "__main__":
    registry = CuratedAssetRegistry()
    
    print("=== Curated Asset Registry ===\n")
    stats = registry.get_stats()
    
    print(f"Library Size: {stats['library_size']}")
    print(f"Available: {stats['available_count']}")
    print(f"Available Icons: {stats['available_icons']}")
    
    # Test resolution
    print("\n--- Testing Resolution ---")
    test_icons = ["cat", "bat", "sun", "dog", "pot", "net", "pig"]
    for icon in test_icons:
        path = registry.resolve(icon, "TEST")
        if path:
            print(f"✅ {icon}: VERIFIED")
        else:
            print(f"❌ {icon}: MISSING (needs @Illustrator)")
