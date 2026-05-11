"""
Centralized project configuration.
Single source of truth for all paths and constants.
"""
from pathlib import Path

# === Project Root ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# === Directory Paths ===
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUT_DIR = PROJECT_ROOT / "output"
ASSETS_DIR = DATA_DIR / "assets"
ICONS_DIR = DATA_DIR / "library" / "assets" / "icons"
TEMPLATES_DIR = DATA_DIR / "assets" / "templates"
OVERLAY_COMPONENTS_DIR = ASSETS_DIR / "overlay_components"
OVERLAYS_DIR = ASSETS_DIR / "overlays"
FINAL_PRODUCTION_DIR = OUTPUT_DIR / "final_production"

# === Config Files ===
SYLLABUS_PATH = PROJECT_ROOT / "project_state.json"
OVERLAY_THEMES_PATH = CONFIG_DIR / "overlay_themes.json"
OVERLAY_SCHEMA_PATH = CONFIG_DIR / "overlay_layout_schema.json"
RIDDLES_PATH = DATA_DIR / "riddles.json"
CHARACTER_CONFIG_PATH = DATA_DIR / "assets" / "characters" / "config.json"

# === Canvas Constants (A4 Landscape @ 300 DPI) ===
A4_WIDTH = 3508
A4_HEIGHT = 2480
