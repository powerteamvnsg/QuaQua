"""
QoK Level 1 - Image Generation Scheduler
=========================================
Schedules and automates icon generation based on quota limits.

Based on master_summary.json, generates all 32 unique icons needed.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# === CONFIGURATION ===

MASTER_SUMMARY = Path(r"D:\moetvnpapers\k2-worksheet-generator\output\QoK_Level1\master_summary.json")
SCHEDULE_OUTPUT = Path(r"D:\moetvnpapers\k2-worksheet-generator\output\QoK_Level1\image_generation_schedule.json")
STYLE_GUIDE = Path(r"D:\moetvnpapers\docs\K2_ILLUSTRATION_STYLE_GUIDE.md")

# Quota limits (based on observed behavior)
IMAGES_PER_QUOTA = 12
QUOTA_RESET_HOURS = 5

# Style Guide v4.3 Prompt Templates
ANIMAL_PROMPT = "Kawaii style {subject}, {view} view, thin black outlines, small dot eyes with tiny white reflection, {color} colors, {pose}, white background, no text"
OBJECT_PROMPT = "Generate Kawaii style objects without faces. {color} {subject}, {view} view, thin black outlines, white background, no text"

# Icon definitions with category and prompt parameters
ICON_DEFINITIONS = {
    # === ANIMALS (with face) ===
    "ant": {"category": "animal", "color": "black and red", "view": "3/4", "pose": "standing"},
    "bat": {"category": "animal", "color": "brown and gray", "view": "3/4", "pose": "flying"},
    "cat": {"category": "animal", "color": "orange", "view": "3/4", "pose": "sitting"},
    "fish": {"category": "animal", "color": "orange and white", "view": "side", "pose": "swimming"},
    "lion": {"category": "animal", "color": "golden", "view": "3/4", "pose": "sitting"},
    "mice": {"category": "animal", "color": "gray", "view": "3/4", "pose": "standing"},
    "mole": {"category": "animal", "color": "brown", "view": "3/4", "pose": "peeking from ground"},
    "rat": {"category": "animal", "color": "gray", "view": "3/4", "pose": "standing"},
    "run": {"category": "animal", "color": "colorful clothes", "view": "side", "pose": "running", "subject": "child running"},
    "sun": {"category": "animal", "color": "yellow and orange", "view": "front", "pose": "shining"},
    
    # === OBJECTS (no face) ===
    "bone": {"category": "object", "color": "white", "view": "3/4"},
    "bow": {"category": "object", "color": "red ribbon", "view": "front"},
    "bronze": {"category": "object", "color": "bronze colored", "view": "3/4", "subject": "bronze medal"},
    "cape": {"category": "object", "color": "red", "view": "3/4", "subject": "superhero cape"},
    "cloud": {"category": "object", "color": "white fluffy", "view": "front"},
    "diamond": {"category": "object", "color": "blue sparkling", "view": "front", "subject": "diamond gem"},
    "flower": {"category": "object", "color": "pink and green", "view": "front"},
    "gold": {"category": "object", "color": "gold shiny", "view": "3/4", "subject": "gold coin"},
    "hat": {"category": "object", "color": "black with red ribbon and bow", "view": "3/4", "subject": "top hat"},
    "ice": {"category": "object", "color": "light blue transparent", "view": "3/4", "subject": "ice cube"},
    "iron": {"category": "object", "color": "silver gray", "view": "3/4", "subject": "iron ingot"},
    "king": {"category": "object", "color": "gold with red velvet", "view": "front", "subject": "royal crown"},
    "lily": {"category": "object", "color": "white and green", "view": "top-down", "subject": "lily flower on lily pad"},
    "nest": {"category": "object", "color": "brown and tan", "view": "3/4", "subject": "bird nest with eggs"},
    "nut": {"category": "object", "color": "brown", "view": "3/4", "subject": "walnut"},
    "pond": {"category": "object", "color": "blue and green", "view": "top-down", "subject": "small pond"},
    "rain": {"category": "object", "color": "blue", "view": "front", "subject": "rain drops"},
    "ring": {"category": "object", "color": "gold with diamond", "view": "3/4", "subject": "diamond ring"},
    "silver": {"category": "object", "color": "silver shiny", "view": "3/4", "subject": "silver coin"},
    "snow": {"category": "object", "color": "white", "view": "front", "subject": "snowflake"},
    "stone": {"category": "object", "color": "gray", "view": "3/4", "subject": "stone pebble"},
    "wind": {"category": "object", "color": "light blue swirl", "view": "side", "subject": "wind swirl lines"},
}


def generate_prompt(icon_name: str) -> str:
    """Generate the appropriate prompt for an icon."""
    if icon_name not in ICON_DEFINITIONS:
        return f"Kawaii style {icon_name}, 3/4 view, thin black outlines, white background, no text"
    
    defn = ICON_DEFINITIONS[icon_name]
    subject = defn.get("subject", icon_name)
    color = defn.get("color", "colorful")
    view = defn.get("view", "3/4")
    pose = defn.get("pose", "")
    
    if defn["category"] == "animal":
        return ANIMAL_PROMPT.format(subject=subject, view=view, color=color, pose=pose)
    else:
        return OBJECT_PROMPT.format(subject=subject, view=view, color=color)


def create_schedule():
    """Create a generation schedule based on quota limits."""
    # Load master summary
    with open(MASTER_SUMMARY, "r") as f:
        summary = json.load(f)
    
    icons = summary["all_unique_icons"]
    total_icons = len(icons)
    
    # Calculate batches
    num_batches = (total_icons + IMAGES_PER_QUOTA - 1) // IMAGES_PER_QUOTA
    
    schedule = {
        "created_at": datetime.now().isoformat(),
        "style_guide": "K2_ILLUSTRATION_STYLE_GUIDE.md v4.3",
        "total_icons": total_icons,
        "images_per_batch": IMAGES_PER_QUOTA,
        "quota_reset_hours": QUOTA_RESET_HOURS,
        "estimated_total_hours": num_batches * QUOTA_RESET_HOURS,
        "batches": []
    }
    
    current_time = datetime.now()
    
    for batch_idx in range(num_batches):
        start_idx = batch_idx * IMAGES_PER_QUOTA
        end_idx = min(start_idx + IMAGES_PER_QUOTA, total_icons)
        batch_icons = icons[start_idx:end_idx]
        
        scheduled_time = current_time + timedelta(hours=batch_idx * QUOTA_RESET_HOURS)
        
        batch = {
            "batch_number": batch_idx + 1,
            "scheduled_time": scheduled_time.isoformat(),
            "icons": []
        }
        
        for icon in batch_icons:
            prompt = generate_prompt(icon)
            category = ICON_DEFINITIONS.get(icon, {}).get("category", "unknown")
            batch["icons"].append({
                "name": icon,
                "category": category,
                "prompt": prompt,
                "status": "pending"
            })
        
        schedule["batches"].append(batch)
    
    # Save schedule
    with open(SCHEDULE_OUTPUT, "w") as f:
        json.dump(schedule, f, indent=2)
    
    # Print summary
    print("=" * 70)
    print("📅 IMAGE GENERATION SCHEDULE")
    print("=" * 70)
    print(f"Total Icons: {total_icons}")
    print(f"Batches: {num_batches}")
    print(f"Images per Batch: {IMAGES_PER_QUOTA}")
    print(f"Estimated Total Time: {schedule['estimated_total_hours']} hours")
    print()
    
    for batch in schedule["batches"]:
        print(f"\n📦 Batch {batch['batch_number']} - {batch['scheduled_time']}")
        print("-" * 50)
        for icon in batch["icons"]:
            print(f"  [{icon['category'][:3].upper()}] {icon['name']}")
    
    print(f"\n✅ Schedule saved to: {SCHEDULE_OUTPUT}")
    
    return schedule


def print_prompts_for_batch(batch_number: int):
    """Print the prompts for a specific batch (for manual generation)."""
    with open(SCHEDULE_OUTPUT, "r") as f:
        schedule = json.load(f)
    
    for batch in schedule["batches"]:
        if batch["batch_number"] == batch_number:
            print(f"\n📦 BATCH {batch_number} PROMPTS")
            print("=" * 70)
            for icon in batch["icons"]:
                print(f"\n### {icon['name'].upper()}")
                print(f"```")
                print(icon["prompt"])
                print(f"```")
            return
    
    print(f"Batch {batch_number} not found.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "prompts":
        batch_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        print_prompts_for_batch(batch_num)
    else:
        create_schedule()
