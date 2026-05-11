"""
Systematic Phonics Curriculum - Visual Generator v3.0
======================================================
PROPERLY positions content within MEASURED panel safe zones.
"""

import json
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "data" / "assets" / "templates"
OUTPUT_DIR = BASE_DIR / "output" / "phonics_worksheets"
CONFIG_PATH = TEMPLATES_DIR / "template_config.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load config
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

# ==========================================
# CURRICULUM
# ==========================================
WORD_FAMILIES = {
    "-at": {"words": ["cat", "bat", "hat", "mat", "rat", "sat", "fat"], "distractors": ["dog", "pig", "log", "sun", "fin"]},
    "-an": {"words": ["can", "fan", "man", "pan", "van", "ran", "tan"], "distractors": ["bed", "lip", "top", "rug", "box"]},
    "-ag": {"words": ["bag", "tag", "wag", "rag", "flag"], "distractors": ["hot", "cup", "zip", "kit", "nut"]},
    "-ad": {"words": ["dad", "sad", "mad", "pad", "bad"], "distractors": ["run", "fog", "wet", "box", "tub"]},
    "-ap": {"words": ["map", "cap", "nap", "tap", "gap", "lap"], "distractors": ["fin", "cot", "net", "tub", "dog"]},
    "-en": {"words": ["hen", "pen", "ten", "men", "den"], "distractors": ["cat", "dig", "rod", "bus", "pot"]},
    "-et": {"words": ["net", "jet", "wet", "pet", "vet", "set"], "distractors": ["fan", "map", "log", "bug", "pan"]},
    "-ed": {"words": ["bed", "red", "fed", "led", "wed"], "distractors": ["pig", "top", "nut", "cap", "fox"]},
    "-eg": {"words": ["leg", "peg", "beg", "egg"], "distractors": ["sun", "hat", "fin", "mom", "bun"]},
    "-ell": {"words": ["bell", "well", "tell", "sell", "yell"], "distractors": ["can", "rug", "pot", "lid", "map"]},
    "-in": {"words": ["pin", "bin", "win", "fin", "tin"], "distractors": ["cat", "bed", "log", "mud", "hop"]},
    "-it": {"words": ["sit", "hit", "kit", "bit", "fit"], "distractors": ["run", "fan", "leg", "dog", "tap"]},
    "-ip": {"words": ["lip", "zip", "dip", "hip", "tip", "rip"], "distractors": ["bat", "web", "fox", "cup", "men"]},
    "-ig": {"words": ["pig", "wig", "dig", "big", "fig"], "distractors": ["net", "pot", "sun", "mat", "hen"]},
    "-id": {"words": ["kid", "lid", "hid", "rid"], "distractors": ["map", "ten", "log", "bus", "jam"]},
    "-op": {"words": ["mop", "top", "hop", "pop", "cop"], "distractors": ["bin", "sat", "wet", "tub", "lid"]},
    "-ot": {"words": ["pot", "hot", "dot", "cot", "lot", "not"], "distractors": ["fin", "red", "bug", "tap", "leg"]},
    "-og": {"words": ["dog", "log", "fog", "jog", "frog", "hog"], "distractors": ["pan", "win", "bed", "nut", "kit"]},
    "-ox": {"words": ["fox", "box", "ox"], "distractors": ["run", "hat", "pen", "dig", "sum"]},
    "-ob": {"words": ["cob", "job", "mob", "sob", "rob"], "distractors": ["net", "lip", "cup", "mat", "hen"]},
    "-ub": {"words": ["tub", "sub", "cub", "rub"], "distractors": ["hat", "pen", "dig", "hot", "mom"]},
    "-un": {"words": ["sun", "run", "bun", "fun"], "distractors": ["top", "leg", "sit", "map", "dog"]},
    "-um": {"words": ["gum", "hum", "drum", "plum"], "distractors": ["rat", "vet", "lid", "cob", "nap"]},
    "-ug": {"words": ["bug", "rug", "mug", "hug", "jug", "tug"], "distractors": ["cat", "pin", "pot", "bed", "fox"]},
    "-ut": {"words": ["nut", "cut", "hut", "shut"], "distractors": ["fin", "bag", "web", "log", "kid"]},
}

QUESTS = [
    {"id": 26, "name": "Pot of Gold Quest", "family": "-ug", "template_key": "pot_of_gold"},
]

TEMPLATE_REGISTRY = {
    "pot_of_gold": {
        "sheet1": TEMPLATES_DIR / "sheet1_3panel.png",
        "sheet2": TEMPLATES_DIR / "sheet2_2panel.png",
    },
}

# ==========================================
# FONTS
# ==========================================
def load_font(size):
    for path in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONTS = {
    "title": load_font(16),
    "header": load_font(14),
    "word": load_font(20),
    "trace": load_font(36),
    "label": load_font(11),
    "small": load_font(9),
}

# ==========================================
# COLORS
# ==========================================
COLORS = {
    "white": (255, 255, 255),
    "dark_green": (0, 80, 0),
    "black": (0, 0, 0),
    "gray": (160, 160, 160),
    "light_blue": (230, 245, 255),
    "blue_outline": (100, 100, 200),
}

# ==========================================
# DRAWING HELPERS
# ==========================================
def draw_icon_box(draw, x, y, size, label):
    """Draw a placeholder icon box with label."""
    # Dashed border effect
    draw.rectangle([x, y, x + size, y + size], 
                   fill=COLORS["light_blue"], 
                   outline=COLORS["blue_outline"], 
                   width=2)
    # Center label
    bbox = draw.textbbox((0, 0), label, font=FONTS["small"])
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x + (size - tw) // 2
    ty = y + (size - th) // 2
    draw.text((tx, ty), label, fill=COLORS["black"], font=FONTS["small"])


def get_content(quest):
    """Generate worksheet content for a quest."""
    data = WORD_FAMILIES[quest["family"]]
    words = data["words"]
    distractors = data["distractors"]
    
    trace = words[:3] if len(words) >= 3 else (words * 3)[:3]
    
    circles = []
    for i in range(3):
        tgt = words[(i + 3) % len(words)] if len(words) > 3 else words[i % len(words)]
        opts = [tgt] + random.sample(distractors, 2)
        random.shuffle(opts)
        circles.append({"target": tgt, "options": opts})
    
    match = random.sample(words, 3)
    sort_ok = words[:4] if len(words) >= 4 else (words * 2)[:4]
    sort_bad = distractors[:4]
    
    return {
        "quest_name": quest["name"],
        "family": quest["family"],
        "trace": trace,
        "circles": circles,
        "match": match,
        "sort_correct": sort_ok,
        "sort_wrong": sort_bad,
    }


# ==========================================
# SHEET 1 GENERATOR
# ==========================================
def generate_sheet1(quest, content):
    """Generate Sheet 1: 3-Panel (Trace, Circle, Match)"""
    template_path = TEMPLATE_REGISTRY[quest["template_key"]]["sheet1"]
    img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    cfg = CONFIG["sheet1_3panel"]
    
    # === TITLE BANNER ===
    tb = cfg["title_banner"]
    draw.text((tb["x"], tb["y"]), content["quest_name"], 
              fill=COLORS["white"], font=FONTS["title"])
    
    # === INSTRUCTION BOX ===
    ib = cfg["instruction_box"]
    draw.text((ib["x"] + 15, ib["y"] + 35), 
              "Name: _________________________", 
              fill=COLORS["dark_green"], font=FONTS["header"])
    
    # === PANEL 1: TRACE IT ===
    p1 = cfg["panel_1"]
    sz = p1["safe_zone"]
    
    # Header
    draw.text((sz["x"] + 5, sz["y"] + p1["header_offset_y"]), 
              "1. Trace It!", fill=COLORS["dark_green"], font=FONTS["header"])
    
    # Content - distribute 3 rows evenly in available height
    content_height = sz["height"] - p1["content_start_y"] - 20
    row_height = content_height // 3
    icon_size = p1["icon_size"]
    
    for i, word in enumerate(content["trace"]):
        y = sz["y"] + p1["content_start_y"] + (i * row_height)
        
        # Icon
        draw_icon_box(draw, sz["x"] + p1["icon_margin_left"], y, icon_size, word)
        
        # Traced word (spaced letters)
        spaced = "   ".join(word.upper())
        text_x = sz["x"] + p1["icon_margin_left"] + icon_size + 15
        text_y = y + (icon_size - 36) // 2
        draw.text((text_x, text_y), spaced, fill=COLORS["gray"], font=FONTS["trace"])
    
    # === PANEL 2: CIRCLE IT ===
    p2 = cfg["panel_2"]
    sz2 = p2["safe_zone"]
    
    # Header
    draw.text((sz2["x"] + 5, sz2["y"] + p2["header_offset_y"]), 
              "2. Circle It!", fill=COLORS["dark_green"], font=FONTS["header"])
    
    content_height = sz2["height"] - p2["content_start_y"] - 20
    row_height = content_height // 3
    opt_size = p2["option_size"]
    
    for i, row in enumerate(content["circles"]):
        y = sz2["y"] + p2["content_start_y"] + (i * row_height)
        
        # Target word
        draw.text((sz2["x"] + 5, y + 15), row["target"].upper(), 
                  fill=COLORS["black"], font=FONTS["word"])
        
        # Options (3 icons horizontally)
        opt_start_x = sz2["x"] + 70
        available_width = sz2["width"] - 80
        opt_gap = (available_width - (3 * opt_size)) // 2
        
        for j, opt in enumerate(row["options"]):
            ox = opt_start_x + j * (opt_size + opt_gap)
            draw_icon_box(draw, ox, y, opt_size, opt)
    
    # === PANEL 3: MATCH IT ===
    p3 = cfg["panel_3"]
    sz3 = p3["safe_zone"]
    
    # Header
    draw.text((sz3["x"] + 5, sz3["y"] + p3["header_offset_y"]), 
              "3. Match It!", fill=COLORS["dark_green"], font=FONTS["header"])
    
    content_height = sz3["height"] - p3["content_start_y"] - 20
    row_height = content_height // 3
    icon_size3 = p3["icon_size"]
    
    # Shuffle right side for puzzle
    right = list(content["match"])
    random.shuffle(right)
    
    for i in range(3):
        y = sz3["y"] + p3["content_start_y"] + (i * row_height)
        
        # Word on left
        draw.text((sz3["x"] + 10, y + 20), content["match"][i].upper(), 
                  fill=COLORS["black"], font=FONTS["word"])
        
        # Connecting line
        line_y = y + 35
        draw.line([(sz3["x"] + 80, line_y), (sz3["x"] + sz3["width"] - icon_size3 - 20, line_y)],
                  fill=COLORS["gray"], width=1)
        
        # Icon on right
        draw_icon_box(draw, sz3["x"] + sz3["width"] - icon_size3 - 10, y, icon_size3, right[i])
    
    # Save
    out = OUTPUT_DIR / f"Q{quest['id']:02d}_Sheet1_{quest['name'].replace(' ', '_')}.png"
    img.save(out)
    print(f"✅ Sheet 1: {out.name}")
    return out


# ==========================================
# SHEET 2 GENERATOR
# ==========================================
def generate_sheet2(quest, content):
    """Generate Sheet 2: 2-Panel (Sort) + Footer Cut-outs"""
    template_path = TEMPLATE_REGISTRY[quest["template_key"]]["sheet2"]
    img = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    cfg = CONFIG["sheet2_2panel"]
    
    # === TITLE BANNER ===
    tb = cfg["title_banner"]
    fam = content["family"].replace("-", "")
    draw.text((tb["x"], tb["y"]), f"Sort: '{fam}' Words", 
              fill=COLORS["white"], font=FONTS["title"])
    
    # === INSTRUCTION BOX ===
    ib = cfg["instruction_box"]
    draw.text((ib["x"] + 15, ib["y"] + 35), 
              "Name: _________________________", 
              fill=COLORS["dark_green"], font=FONTS["header"])
    
    # === LEFT PANEL: Target Family ===
    pl = cfg["panel_left"]
    szl = pl["safe_zone"]
    
    # Header
    draw.text((szl["x"] + 10, szl["y"] + pl["header_offset_y"]), 
              f"Words ending in {content['family']}", 
              fill=COLORS["dark_green"], font=FONTS["header"])
    
    # Grid of 4 drop slots (2x2)
    slot_size = pl["slot_size"]
    gap = pl["slot_gap"]
    grid_width = 2 * slot_size + gap
    grid_height = 2 * slot_size + gap
    
    # Center the grid
    grid_x = szl["x"] + (szl["width"] - grid_width) // 2
    grid_y = szl["y"] + pl["grid_start_y"]
    
    for row in range(2):
        for col in range(2):
            x = grid_x + col * (slot_size + gap)
            y = grid_y + row * (slot_size + gap)
            draw.rectangle([x, y, x + slot_size, y + slot_size], 
                          outline=COLORS["blue_outline"], width=2)
    
    # === RIGHT PANEL: Other Words ===
    pr = cfg["panel_right"]
    szr = pr["safe_zone"]
    
    # Header
    draw.text((szr["x"] + 10, szr["y"] + pr["header_offset_y"]), 
              "Other Words", 
              fill=COLORS["dark_green"], font=FONTS["header"])
    
    # Grid of 4 drop slots (2x2)
    grid_x = szr["x"] + (szr["width"] - grid_width) // 2
    grid_y = szr["y"] + pr["grid_start_y"]
    
    for row in range(2):
        for col in range(2):
            x = grid_x + col * (slot_size + gap)
            y = grid_y + row * (slot_size + gap)
            draw.rectangle([x, y, x + slot_size, y + slot_size], 
                          outline=COLORS["blue_outline"], width=2)
    
    # === FOOTER: Cut-outs ===
    fc = cfg["footer"]
    
    # Scissor line
    draw.text((400, fc["y"] - 18), "✂️ Cut out and glue above ✂️", 
              fill=COLORS["dark_green"], font=FONTS["small"])
    draw.line([(50, fc["y"] - 5), (900, fc["y"] - 5)], fill=COLORS["gray"], width=1)
    
    # 8 cut-out items
    cuts = content["sort_correct"] + content["sort_wrong"]
    random.shuffle(cuts)
    
    for i, label in enumerate(cuts[:fc["item_count"]]):
        x = fc["start_x"] + i * fc["gap"]
        draw_icon_box(draw, x, fc["y"], fc["item_size"], label)
    
    # Save
    out = OUTPUT_DIR / f"Q{quest['id']:02d}_Sheet2_{quest['name'].replace(' ', '_')}.png"
    img.save(out)
    print(f"✅ Sheet 2: {out.name}")
    return out


# ==========================================
# MAIN
# ==========================================
def generate_quest(quest_id):
    quest = next((q for q in QUESTS if q["id"] == quest_id), None)
    if not quest:
        print(f"❌ Quest {quest_id} not found")
        return
    
    print(f"\n📖 Generating: {quest['name']} ({quest['family']})")
    print("-" * 50)
    
    content = get_content(quest)
    s1 = generate_sheet1(quest, content)
    s2 = generate_sheet2(quest, content)
    
    # Manifest
    manifest = {
        "quest_id": quest_id,
        "quest_name": quest["name"],
        "family": quest["family"],
        "generated_at": datetime.now().isoformat(),
        "sheets": {
            "sheet1": str(s1),
            "sheet2": str(s2),
            "sheet3": "MANUAL"
        }
    }
    
    mp = OUTPUT_DIR / f"Q{quest_id:02d}_manifest.json"
    with open(mp, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"📋 Manifest: {mp.name}")
    print("✅ Generation complete!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generate_quest(int(sys.argv[1]))
    else:
        generate_quest(26)  # Pot of Gold Quest
