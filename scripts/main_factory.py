
import argparse
import json
import sys
from pathlib import Path

# --- Import your modules ---
from src.pipeline.asset_manager import AssetManager
from src.pipeline.draft_generator import DraftGenerator
from src.compositor.layout_engine import LayoutEngine

# --- Configuration Paths ---
THEMES_CONFIG_PATH = Path("config/overlay_themes.json")
LAYOUT_SCHEMA_PATH = Path("config/overlay_layout_schema.json")
OUTPUT_BASE_PATH = Path("output")

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Configuration file not found at {path}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Master Factory: Storytelling Mode")
    parser.add_argument("--theme", type=str, required=True, help="Theme key (e.g., 'pirate')")
    args = parser.parse_args()
    theme_key = args.theme.lower()
    
    # 1. Load Data
    themes_data = load_config(THEMES_CONFIG_PATH)
    if theme_key not in themes_data:
        print(f"❌ Theme '{theme_key}' not found.")
        sys.exit(1)

    current_theme = themes_data[theme_key]
    
    # 2. Initialize Agents
    asset_manager = AssetManager(output_dir=OUTPUT_BASE_PATH / f"{theme_key}_assets")
    layout_engine = LayoutEngine(schema_path=LAYOUT_SCHEMA_PATH, output_dir=OUTPUT_BASE_PATH)

    print(f"\n🏴‍☠️ STARTING STORY FACTORY: [{theme_key.upper()}]")
    story_seq = current_theme.get('story_sequence', [])
    print(f"   Story Arc: {len(story_seq)} Scenes Detected\n")

    # 3. Comprehensive Asset & Draft Manager
    ready_assets = {}
    
    print("   🔍 Verifying Asset manifest...")
    
    # A. Banner
    b_prompt = current_theme['banner_prompt']
    b_path = Path(asset_manager.get_or_create("banner", b_prompt, current_theme['style_tokens']))
    if not b_path.exists():
        DraftGenerator.create_placeholder(b_path, "Banner", b_prompt, 1600, 600)
    ready_assets['banner'] = str(b_path)

    # B. Scenes
    for scene in story_seq:
        s_id = scene['phase']
        s_prompt = scene['frame_prompt']
        s_path = Path(asset_manager.get_or_create(f"frame_{s_id}", s_prompt, current_theme['style_tokens']))
        
        if not s_path.exists():
            DraftGenerator.create_placeholder(s_path, f"Scene {s_id}", s_prompt, 2750, 1500)
        
        ready_assets[s_id] = str(s_path)

    # 4. Assembly Phase
    print("\n" + "="*60)
    print("✨ ALL STREAMS READY. ASSEMBLING STORYBOOKS...")
    print("="*60)

    for scene in story_seq:
        s_id = scene['phase']
        print(f"   🧩 Building Sheet: {scene['description']}...")
        
        sheet_assets = {
            'scene': ready_assets[s_id],
            'banner': ready_assets['banner']
        }
        
        final_path = layout_engine.assemble(
            theme_name=f"{theme_key}_{s_id}",
            assets=sheet_assets
        )
        print(f"      -> Final Result: {final_path}")

    print("\n✅ STORY ASSEMBLY COMPLETE! Check production folder.")

if __name__ == "__main__":
    main()
