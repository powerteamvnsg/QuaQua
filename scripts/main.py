import os
import json
import argparse
from modular_factory import WorksheetFactory
from src.config import SYLLABUS_PATH, ICONS_DIR

# CONFIG
STATE_FILE = str(SYLLABUS_PATH)
PROMPT_FILE = "agent_todo_list.txt"

def get_missing_icons(syllabus):
    """Scans for missing assets using strict file matching."""
    available_icons = set()
    for root, dirs, files in os.walk(ICONS_DIR):
        for f in files:
            if f.endswith(".png"):
                available_icons.add(f.lower())
    
    missing_map = {}
    for quest in syllabus:
        words = quest.get('words', [])
        missing = [w for w in words if f"{w}.png".lower() not in available_icons]
        if missing:
            missing_map[quest['name']] = missing
    return missing_map

def generate_prompts(missing_map):
    """Generates a text file for the Visual Agent."""
    if not missing_map:
        print("✅ No missing icons! The Art Agent is not needed.")
        return

    print(f"⚠️ Found missing assets. Generating '{PROMPT_FILE}'...")
    
    with open(PROMPT_FILE, "w") as f:
        f.write("# URGENT ASSET REQUEST FOR ART AGENT\n")
        f.write("Please generate the following 'Kawaii' style icons.\n")
        f.write("Style Rules: Thin black outlines, flat colors, white shine dot in eyes, no background.\n\n")
        
        for quest_name, icons in missing_map.items():
            f.write(f"## Context: {quest_name}\n")
            for icon in icons:
                f.write(f"1. [ICON]: {icon} -> Generate a cute, simple illustration of a {icon}.\n")
            f.write("\n")
    
    print(f"📄 Bridge created: Open '{PROMPT_FILE}' and give it to your Art Agent.")


def audit_mode(export_prompts=False):
    print("--- 📋 STARTING PROJECT AUDIT ---")
    if not os.path.exists(STATE_FILE):
        print(f"❌ CRITICAL: {STATE_FILE} not found!")
        return

    with open(STATE_FILE, "r") as f:
        syllabus = json.load(f)

    missing_map = get_missing_icons(syllabus)
    
    ready_count = 0
    for quest in syllabus:
        name = quest.get('name', 'Unknown')
        missing = missing_map.get(name, [])
        
        # Check Word Count (Min 3)
        word_count_ok = len(quest.get('words', [])) >= 3
        
        status = "✅"
        msg = "READY"
        
        if not word_count_ok:
            status = "❌"
            msg = "TOO FEW WORDS (Need 3+)"
        elif missing:
            status = "⚠️"
            msg = f"MISSING ICONS: {missing}"
        
        if status == "✅": ready_count += 1
        print(f"{status} [{quest.get('id')}] {name.ljust(30)} | {msg}")

    print("-" * 50)
    print(f"📊 STATUS: {ready_count}/{len(syllabus)} Quests Ready.")
    
    if export_prompts and missing_map:
        generate_prompts(missing_map)

def build_mode(specific_id=None):
    print("--- 🏭 STARTING BUILD PROCESS ---")
    if not os.path.exists(STATE_FILE): return

    factory = WorksheetFactory(STATE_FILE)
    for quest in factory.syllabus:
        if specific_id and quest['id'] != specific_id: continue
        try:
            print(f"   Building {quest['id']} ({quest['name']})...")
            factory.generate_sheet_1(quest)
            factory.generate_sheet_2(quest)
        except Exception as e:
            print(f"   🔴 Error {quest['id']}: {e}")
    print("\n✅ Build Complete. Check output_modular_build/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="K2 Worksheet Orchestrator")
    parser.add_argument("--audit", action="store_true", help="Check curriculum status")
    parser.add_argument("--prompts", action="store_true", help="Generate Art Agent Todo List")
    parser.add_argument("--build", action="store_true", help="Generate PNGs")
    parser.add_argument("--quest", type=str, help="Target specific Quest ID")

    args = parser.parse_args()

    if args.audit or args.prompts:
        audit_mode(export_prompts=args.prompts)
    elif args.build or args.quest:
        build_mode(args.quest)
    else:
        print("Usage: python main.py [--audit | --prompts | --auto-art | --build]")
