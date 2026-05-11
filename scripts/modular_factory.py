import os
import random
import json
from PIL import Image, ImageDraw, ImageFont
from src.config import (
    PROJECT_ROOT, ICONS_DIR, OVERLAYS_DIR, RIDDLES_PATH,
    A4_WIDTH, A4_HEIGHT
)

# ==========================================
# 1. CONFIGURATION
# ==========================================
OUTPUT_DIR = "output_modular_build"
FONT_DIR = str(PROJECT_ROOT / "data" / "assets" / "fonts")

# CANVAS
WIDTH, HEIGHT = A4_WIDTH, A4_HEIGHT
BG_COLOR = "white"

# COLORS
COLOR_TRACE = (200, 200, 200)
COLOR_TEXT = (50, 50, 50)
COLOR_GREEN = (34, 139, 34) # User Choice: Borders stay Green
COLOR_BROWN = (139, 69, 19)

# TYPOGRAPHY
SIZE_TITLE_NAME = 125
SIZE_TITLE_QUEST = 175
SIZE_INSTR = 65
SIZE_INSTR_S1 = 50
SIZE_INSTR_FAMILY_S1 = 60
SIZE_TRACE = 150
SIZE_LABEL = 85
SIZE_FAMILY = 200

# PREPARE FONTS
try:
    PATH_TRACE = os.path.join(FONT_DIR, "dotrice", "hdad-dotrice-1.001", "Dotrice-Regular.otf")
    PATH_TITLE = os.path.join(FONT_DIR, "childhood", "Childhood-Bold.otf")
    PATH_BODY = os.path.join(FONT_DIR, "splendid-plan-9", "Splendid Plan 9 Regular.ttf")
    PATH_LABEL = os.path.join(FONT_DIR, "street", "STREET__.ttf")

    font_trace = ImageFont.truetype(PATH_TRACE, SIZE_TRACE)
    font_title_name = ImageFont.truetype(PATH_TITLE, SIZE_TITLE_NAME)
    font_title_quest = ImageFont.truetype(PATH_TITLE, SIZE_TITLE_QUEST)
    font_label = ImageFont.truetype(PATH_LABEL, SIZE_LABEL)
    font_instr = ImageFont.truetype(PATH_BODY, SIZE_INSTR)
    font_instr_s1 = ImageFont.truetype(PATH_BODY, SIZE_INSTR_S1)
    font_instr_family_s1 = ImageFont.truetype(PATH_BODY, SIZE_INSTR_FAMILY_S1)
    font_family = ImageFont.truetype(PATH_BODY, SIZE_FAMILY)
except Exception as e:
    print(f"Warning: Missing specific fonts {e}. Using defaults.")
    font_trace = font_title_name = font_title_quest = font_label = ImageFont.load_default()
    font_instr = font_instr_s1 = font_instr_family_s1 = font_family = ImageFont.load_default()

# LAYOUT DEFINITIONS
LAYOUT = {
    "HEADER": {
        "TITLE": {"x": 250, "y": 120, "w": 1070, "h": 430}, # formatting matches s1 logic
        "INSTR": {"x": 1670, "y": 145, "w": 1280, "h": 430}
    },
    "S1_PANELS": {
        "A": {"x": 250, "y": 640, "w": 976, "h": 1600},
        "B": {"x": 1266, "y": 640, "w": 976, "h": 1600},
        "C": {"x": 2282, "y": 640, "w": 976, "h": 1350} 
    },
    "S2_PANELS": {
        "D": {"x": 250, "y": 640, "w": 1480, "h": 1600},
        "E": {"x": 1780, "y": 640, "w": 1480, "h": 1600}
    }
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def get_icon_image(word):
    target = f"{word}.png".lower()
    if os.path.exists(os.path.join(ICONS_DIR, target)):
        return Image.open(os.path.join(ICONS_DIR, target)).convert("RGBA")
    for root, _, files in os.walk(ICONS_DIR):
        if target in [f.lower() for f in files]:
            return Image.open(os.path.join(root, target)).convert("RGBA")
    return None

def paste_centered(bg, fg, cx, cy, max_size):
    w, h = fg.size
    ratio = min(max_size / w, max_size / h)
    new_size = (int(w * ratio), int(h * ratio))
    fg_resized = fg.resize(new_size, Image.Resampling.LANCZOS)
    px = int(cx - new_size[0] / 2)
    py = int(cy - new_size[1] / 2)
    bg.alpha_composite(fg_resized, (px, py))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        try: w = font.getlength(test_line)
        except Exception: w = len(test_line) * 10
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line: lines.append(' '.join(current_line))
            current_line = [word]
    if current_line: lines.append(' '.join(current_line))
    return '\n'.join(lines)

# ==========================================
# 3. ACTIVITY REGISTRY (WIDGETS)
# ==========================================

def render_activity_trace_stack(draw, rect, i, words, aux):
    pass 

# ==========================================
# 4. MODULAR GENERATOR CLASS
# ==========================================
class WorksheetFactory:
    def __init__(self, syllabus_path):
        with open(syllabus_path, "r") as f:
            self.syllabus = json.load(f)
        try:
             with open(RIDDLES_PATH, "r") as f:
                self.riddles = json.load(f)
        except Exception:
            self.riddles = {}
            
        self.all_words = []
        for q in self.syllabus:
            self.all_words.extend(q['words'])
            
    def get_distractors(self, count, exclude=[]):
        pool = [w for w in self.all_words if w not in exclude]
        return random.sample(pool, min(count, len(pool)))

    def render_header_s1(self, draw, quest):
        # Title
        t_box = LAYOUT["HEADER"]["TITLE"]
        t_cx = t_box["x"] + t_box["w"] // 2
        t_cy = t_box["y"] + t_box["h"] // 2
        
        display_name = quest['name'].replace(" Quest", "").replace(" quest", "").strip()
        gap = 10
        total_h = SIZE_TITLE_NAME + SIZE_TITLE_QUEST + gap
        start_y = t_cy - (total_h // 2)
        
        draw.text((t_cx, start_y), display_name, fill="black", font=font_title_name, anchor="mt")
        draw.text((t_cx, start_y + SIZE_TITLE_NAME + gap), "Quest", fill="black", font=font_title_quest, anchor="mt")
        
        # Instructions S1
        i_box = LAYOUT["HEADER"]["INSTR"]
        i_x = i_box["x"] + 30 
        header_start_y = i_box["y"] + 60
        
        # "Today you'll learn about [FAMILY] sounds."
        part1 = "Today you'll learn about "
        part2 = quest['target'] # e.g. "at"
        part3 = " sounds."
        
        draw.text((i_x, header_start_y), part1, fill=COLOR_TEXT, font=font_instr_s1, anchor="lt")
        w1 = font_instr_s1.getlength(part1)
        draw.text((i_x + w1, header_start_y - 5), part2, fill=COLOR_GREEN, font=font_instr_family_s1, anchor="lt")
        w2 = font_instr_family_s1.getlength(part2)
        draw.text((i_x + w1 + w2, header_start_y), part3, fill=COLOR_TEXT, font=font_instr_s1, anchor="lt")
        w3 = font_instr_s1.getlength(part3)
        
        line_y = header_start_y + font_instr_s1.getmetrics()[0] + 10
        draw.line([(i_x, line_y), (i_x + w1 + w2 + w3, line_y)], fill=COLOR_TEXT, width=3)
        
        # Body Lines
        variant = quest.get('variant_s1', 'Standard')
        
        line_1 = "1. Trace the word of the picture you see."
        if variant == 'S1-A':
            # Starter: Fill in onset
            line_1 = "1. Write the missing letters for each picture."
        elif variant == 'S1-B':
            # Scrambler: Unscramble
            line_1 = "1. Unscramble the letters and write the word below."
        elif variant == 'S1-C':
            # Selector: Circle Correct
            line_1 = "1. Read the word and circle the matching picture."
        elif variant == 'S1-D':
            # Logician: Odd One Out
            line_1 = "1. Circle the picture that does not rhyme."
        elif variant == 'S1-E':
            # Creator: Grid + Draw
            line_1 = "1. Find the words in the puzzle."
            # We might want custom lines 2/3 for this variant too
            
        body_lines = [
            line_1,
            "2. Read the word and circle the correct picture." if variant != 'S1-E' else "2. Use the list to help you find them.",
            "3. Match the words to their pictures." if variant != 'S1-E' else "3. Read the words and draw the pictures."
        ]
        curr_y = line_y + 30
        for line in body_lines:
            draw.text((i_x, curr_y), line, fill=COLOR_TEXT, font=font_instr_s1, anchor="lt")
            curr_y += 70

    def render_panel_a_standard(self, canvas, draw, rect, words):
        """Standard Trace Stack Activity"""
        for i in range(3):
            w_idx = i % len(words)
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            
            # Icon Left
            icon_x = rect['x'] + (rect['w'] * 0.30)
            icon_y = row_cy - 40
            icon = get_icon_image(words[w_idx])
            if icon: paste_centered(canvas, icon, int(icon_x), icon_y, 180)
            
            # Trace Right
            trace_text = words[w_idx].upper()
            trace_x = rect['x'] + (rect['w'] * 0.70)
            line_gap = 220
            # Center gap on icon_y
            for t_off in [-line_gap // 2, line_gap // 2]:
                draw.text((trace_x, icon_y + t_off), trace_text, fill=COLOR_TRACE, font=font_trace, anchor="mm")
                
            # Trace Below (Aligned under icon)
            draw.text((int(icon_x), row_cy + 160), trace_text, fill=COLOR_TRACE, font=font_trace, anchor="mm")

    def render_panel_a_starter(self, canvas, draw, rect, words):
        """S1-A: The Starter (Fill-in Onset)"""
        # Display: Icon Left, "_at" Right. Student writes 'c', 'b', etc.
        for i in range(3):
            w_idx = i % len(words)
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            
            # Icon Left
            icon_x = rect['x'] + (rect['w'] * 0.30)
            icon = get_icon_image(words[w_idx])
            if icon: paste_centered(canvas, icon, int(icon_x), row_cy, 180)
            
            # Text Right: "_at"
            word = words[w_idx].lower()
            if len(word) > 1:
                # Remove first char
                stem = word[1:] 
                display_text = f"_{stem}"
            else:
                display_text = "_"
                
            text_x = rect['x'] + (rect['w'] * 0.70)
            
            # Draw the stem part in Black
            # We want the underscore to be a writing line.
            # Let's draw a literal line for the first char and then the text.
            
            # Measure specific parts? 
            # Simple approach: Draw "_at" using the trace font or label font?
            # Instructions say "Write 'b', 'c'". So we provide the line.
            
            # Using trace font for the stem? Or solid black label font?
            # "Student writes". So we show the stem clearly.
            
            # Draw stem text aligned slightly right
            stem_font = font_trace # Keep consistent style or use solid?
            # Let's use solid for the known part if we want them to focus on the missing part.
            # But the user might want tracing style for the stem?
            # Plan says: "Display _at... Student writes 'c'".
            # Let's use the solid Label font for the provided part to show it's "fixed".
            
            draw.text((text_x, row_cy), stem, fill="black", font=font_label, anchor="lm")
            
            # Draw writing line before the stem
            stem_w = font_label.getlength(stem)
            line_end_x = text_x - 10
            line_start_x = line_end_x - 100
            line_y = row_cy + 30 # Baseline approx
            
            draw.line([(line_start_x, line_y), (line_end_x, line_y)], fill="black", width=5)

    def render_panel_a_scrambler(self, canvas, draw, rect, words):
        """S1-B: The Scrambler (Unscramble Word)"""
        for i in range(3):
            w_idx = i % len(words)
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            
            # Icon Left
            icon_x = rect['x'] + (rect['w'] * 0.30)
            icon = get_icon_image(words[w_idx])
            if icon: paste_centered(canvas, icon, int(icon_x), row_cy, 180)
            
            # Scrambled Text Right
            word = words[w_idx].upper()
            chars = list(word)
            # Ensure it's actually scrambled (if length > 1)
            if len(chars) > 1:
                while "".join(chars) == word: random.shuffle(chars)
            scrambled = "  ".join(chars)
            
            text_x = rect['x'] + (rect['w'] * 0.70)
            draw.text((text_x, row_cy), scrambled, fill="black", font=font_label, anchor="mm")
            
            # Writing Line Below (Centered)
            panel_cx = rect['x'] + (rect['w'] // 2)
            line_y = row_cy + 160
            draw.line([(panel_cx - 150, line_y), (panel_cx + 150, line_y)], fill="black", width=5)

    def render_panel_a_selector(self, canvas, draw, rect, words, distractors):
        """S1-C: The Selector (Circle Correct Icon)"""
        for i in range(3):
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            panel_cx = rect['x'] + (rect['w'] // 2)
            
            w_idx = i % len(words)
            target = words[w_idx]
            
            # Word Top
            label_y = row_cy - 100
            draw.text((panel_cx, label_y), target.upper(), fill="black", font=font_label, anchor="mm")
            
            # Icons Below (1 Target, 1 Distractor)
            d = random.choice([x for x in distractors if x != target])
            opts = [target, d]
            random.shuffle(opts)
            
            spacing = 220
            icons_y = row_cy + 80
            for j, opt in enumerate(opts):
                off_x = (j - 0.5) * spacing
                ic = get_icon_image(opt)
                if ic: paste_centered(canvas, ic, int(panel_cx + off_x), icons_y, 160)

    def render_panel_a_logician(self, canvas, draw, rect, words, distractors):
        """S1-D: The Logician (Odd One Out)"""
        for i in range(3):
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            panel_cx = rect['x'] + (rect['w'] // 2)
            
            # 2 Family Words, 1 Distractor
            w_idx = i % len(words)
            target = words[w_idx]
            # Pick another family member (ensure it exists and isn't same? usually 3 words)
            others = [w for w in words if w != target]
            if not others: others = [target] # Fallback
            partner = random.choice(others)
            
            d = random.choice([x for x in distractors if x not in words])
            
            opts = [target, partner, d]
            random.shuffle(opts)
            
            # Display 3 icons (Triangle or Row?)
            # Row fits well
            spacing = 220
            for j, opt in enumerate(opts):
                # j=0: -1, j=1: 0, j=2: 1
                off_x = (j - 1) * spacing
                ic = get_icon_image(opt)
                if ic: paste_centered(canvas, ic, int(panel_cx + off_x), row_cy, 150)

    def render_panel_a_grid(self, canvas, draw, rect, words):
        """S1-E: 4x4 Word Search Grid"""
        # 1. Generate Grid
        grid_size = 4
        grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Place words
        for word in words:
            w = word.upper()
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    r = random.randint(0, grid_size - 1)
                    c = random.randint(0, grid_size - len(w))
                    # Check fit
                    fits = True
                    for k in range(len(w)):
                        if grid[r][c+k] != '' and grid[r][c+k] != w[k]:
                            fits = False
                            break
                    if fits:
                        for k in range(len(w)): grid[r][c+k] = w[k]
                        placed = True
                else: # V
                    r = random.randint(0, grid_size - len(w))
                    c = random.randint(0, grid_size - 1)
                    fits = True
                    for k in range(len(w)):
                        if grid[r+k][c] != '' and grid[r+k][c] != w[k]:
                            fits = False
                            break
                    if fits:
                        for k in range(len(w)): grid[r+k][c] = w[k]
                        placed = True
                attempts += 1
                
        # Fill empty
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == '':
                    grid[r][c] = random.choice(ALPHABET)
                    
        # 2. Render Grid
        # Calculate cell size
        margin = 60
        g_w = rect['w'] - (2 * margin)
        cell_size = g_w // grid_size
        start_x = rect['x'] + margin
        
        # Vertical centering
        g_h = cell_size * grid_size
        start_y = rect['y'] + (rect['h'] - g_h) // 2
        
        for r in range(grid_size):
            for c in range(grid_size):
                cx = start_x + (c * cell_size) + (cell_size // 2)
                cy = start_y + (r * cell_size) + (cell_size // 2)
                
                # Draw cell border (optional, maybe light gray)
                x1 = start_x + (c * cell_size)
                y1 = start_y + (r * cell_size)
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                draw.rectangle((x1, y1, x2, y2), outline=(200, 200, 200), width=2)
                
                # Draw Letter
                draw.text((cx, cy), grid[r][c], fill="black", font=font_label, anchor="mm")

    def render_panel_b_search_list(self, canvas, draw, rect, words):
        """S1-E: List of words/icons to find"""
        for i in range(3):
            w_idx = i % len(words)
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            panel_cx = rect['x'] + (rect['w'] // 2)
            
            # Icon Left, Word Right
            # Or Stacked?
            # Standard look: Icon Left ~30%, Word Right ~70%
            icon_x = rect['x'] + (rect['w'] * 0.30)
            text_x = rect['x'] + (rect['w'] * 0.70)
            
            ic = get_icon_image(words[w_idx])
            if ic: paste_centered(canvas, ic, int(icon_x), row_cy, 160)
            
            draw.text((text_x, row_cy), words[w_idx].upper(), fill="black", font=font_label, anchor="mm")

    def render_panel_c_draw(self, canvas, draw, rect, words):
        """S1-E: Read and Draw"""
        for i in range(3):
            w_idx = i % len(words)
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            
            # Layout: Word on Left (small), Big Empty Box on Right
            word_x = rect['x'] + (rect['w'] * 0.20)
            draw.text((word_x, row_cy), words[w_idx].upper(), fill="black", font=font_label, anchor="mm")
            
            # Drawing Box
            box_x = rect['x'] + (rect['w'] * 0.45)
            box_w = rect['w'] * 0.45
            box_h = row_h * 0.8
            box_y = row_cy - (box_h // 2)
            
            draw.rectangle(
                [box_x, box_y, box_x + box_w, box_y + box_h], 
                outline="black", width=3
            )
            # Maybe dashed? standard PIL doesn't do dashed lines easily for rects without plugin/logic
            # Solid box is fine for drawing instructions.

    def render_panel_b_standard(self, canvas, draw, rect, words, distractors):
        """Standard Circle Correct Activity"""
        for i in range(3):
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            panel_cx = rect['x'] + (rect['w'] // 2)
            
            target = words[(i+1) % len(words)] # Shifted target
            
            # Word Top
            label_y = row_cy - 100
            draw.text((panel_cx, label_y), target.upper(), fill="black", font=font_label, anchor="mm")
            
            # Icons Below
            d = random.choice([x for x in distractors if x != target])
            opts = [target, d]
            random.shuffle(opts)
            
            spacing = 220
            icons_y = row_cy + 80
            for j, opt in enumerate(opts):
                off_x = (j - 0.5) * spacing
                ic = get_icon_image(opt)
                if ic: paste_centered(canvas, ic, int(panel_cx + off_x), icons_y, 160)

    def render_panel_c_standard(self, canvas, draw, rect, words):
        """Standard Match Activity"""
        for i in range(3):
            row_h = rect['h'] // 3
            row_cy = rect['y'] + (i * row_h) + (row_h // 2)
            
            mw = words[:3]
            mi = list(words[:3])
            random.shuffle(mi)
            
            word_x = rect['x'] + (rect['w'] * 0.15)
            icon_x = rect['x'] + (rect['w'] * 0.85)
            
            draw.text((word_x, row_cy), mw[i].upper(), fill="black", font=font_label, anchor="mm")
            ic = get_icon_image(mi[i])
            if ic: paste_centered(canvas, ic, int(icon_x), row_cy, 150)

    def generate_sheet_1(self, quest):
        print(f"Generating Modular S1: {quest['name']}")
        canvas = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # Draw Background Panels
        for k in ["A", "B", "C"]:
            p = LAYOUT["S1_PANELS"][k]
            draw.rounded_rectangle(
                [p['x'], p['y'], p['x']+p['w'], p['y']+p['h']], 
                radius=60, outline=COLOR_GREEN, width=20
            )
            
        # Draw Activities (Modular Calls)
        distractors = self.get_distractors(10, exclude=quest['words'])
        
        # Check for Variants (Mock logic for now, or real if passed)
        # You can eventually pass this in 'quest' dict from init_brain.py
        variant = quest.get('variant_s1', 'Standard') # Default to Standard
        
        if variant == 'S1-A':
            self.render_panel_a_starter(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'])
            self.render_panel_b_standard(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'], distractors)
            self.render_panel_c_standard(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        elif variant == 'S1-B':
            self.render_panel_a_scrambler(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'])
            self.render_panel_b_standard(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'], distractors)
            self.render_panel_c_standard(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        elif variant == 'S1-C':
            self.render_panel_a_selector(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'], distractors)
            self.render_panel_b_standard(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'], distractors)
            self.render_panel_c_standard(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        elif variant == 'S1-D':
            self.render_panel_a_logician(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'], distractors)
            self.render_panel_b_standard(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'], distractors)
            self.render_panel_c_standard(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        elif variant == 'S1-E':
            self.render_panel_a_grid(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'])
            self.render_panel_b_search_list(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'])
            self.render_panel_c_draw(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        else:
            self.render_panel_a_standard(canvas, draw, LAYOUT["S1_PANELS"]["A"], quest['words'])
            self.render_panel_b_standard(canvas, draw, LAYOUT["S1_PANELS"]["B"], quest['words'], distractors)
            self.render_panel_c_standard(canvas, draw, LAYOUT["S1_PANELS"]["C"], quest['words'])
        
        # Overlay - Paste this BEFORE header!
        ov_path = os.path.join(OVERLAYS_DIR, f"overlay_{quest['id']}.png")
        if os.path.exists(ov_path):
            try:
                ov = Image.open(ov_path).convert("RGBA").resize((WIDTH, HEIGHT))
                # Use Image.alpha_composite class method for reliability
                canvas = Image.alpha_composite(canvas, ov)
            except Exception as e:
                print(f"Overlay error: {e}")
        
        # Draw Header LAST (So it sits on top of overlay)
        # Re-create draw object because canvas is now a new object/reference
        draw = ImageDraw.Draw(canvas)
        self.render_header_s1(draw, quest)
            
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
        canvas.save(os.path.join(OUTPUT_DIR, f"{quest['id']}_Sheet1_Modular.png"))

    def render_header_s2(self, draw, quest):
        t_box = LAYOUT["HEADER"]["TITLE"]
        t_cx = t_box["x"] + t_box["w"] // 2
        t_cy = t_box["y"] + t_box["h"] // 2
        
        display_name = quest['name'].replace(" Quest", "").replace(" quest", "").strip()
        gap = 10
        total_h = SIZE_TITLE_NAME + SIZE_TITLE_QUEST + gap
        start_y = t_cy - (total_h // 2)
        
        draw.text((t_cx, start_y), display_name, fill="black", font=font_title_name, anchor="mt")
        draw.text((t_cx, start_y + SIZE_TITLE_NAME + gap), "Quest", fill="black", font=font_title_quest, anchor="mt")
        
        i_box = LAYOUT["HEADER"]["INSTR"]
        instr_text = "It's time to get your scissors and glue ready! Cut-out the pictures from the cutout page and glue them in the correct box!"
        
        wrapped = wrap_text(instr_text, font_instr_s1, i_box["w"])
        draw.multiline_text((i_box["x"], i_box["y"]), wrapped, fill=COLOR_TEXT, font=font_instr_s1, spacing=15)


    def render_panel_d_riddles(self, canvas, draw, rect, words, distractors):
        draw.text((rect['x'] + rect['w']//2, rect['y'] + 60), "Read and Solve", fill="black", font=font_label, anchor="mt")
        start_y = rect['y'] + 200; gap = 400 
        for i, word in enumerate(words):
            y_pos = start_y + (i * gap)
            riddle = self.riddles.get(word, f"I am a {word}.")
            wrapped = wrap_text(riddle, font_instr, rect['w'] - 100)
            draw.text((rect['x'] + 50, y_pos), f"{i+1}. {wrapped}", fill="black", font=font_instr, anchor="lt")
            line_y = y_pos + 200
            draw.line([(rect['x'] + 100, line_y), (rect['x'] + rect['w'] - 100, line_y)], fill="black", width=3)

    def render_panel_e_wordsearch(self, canvas, draw, rect, words):
        draw.text((rect['x'] + rect['w']//2, rect['y'] + 60), "Word Search", fill="black", font=font_label, anchor="mt")
        grid_size = 10; grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]
        for word in words:
            w = word.upper(); placed = False; attempts = 0
            while not placed and attempts < 100:
                direction = random.choice(['H', 'V', 'D']); r = random.randint(0, grid_size - 1); c = random.randint(0, grid_size - 1)
                dr, dc = 0, 0
                if direction == 'H': dc = 1
                elif direction == 'V': dr = 1
                elif direction == 'D': dr, dc = 1, 1
                if r + dr*(len(w)-1) < grid_size and c + dc*(len(w)-1) < grid_size:
                    if all(grid[r+k*dr][c+k*dc] in ['', w[k]] for k in range(len(w))):
                        for k in range(len(w)): grid[r+k*dr][c+k*dc] = w[k]
                        placed = True
                attempts += 1
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == '': grid[r][c] = random.choice(ALPHABET)
        margin = 100; g_w = rect['w'] - (2 * margin); cell_size = g_w // grid_size
        start_x = rect['x'] + margin; g_h = cell_size * grid_size; start_y = rect['y'] + (rect['h'] - g_h) // 2
        for r in range(grid_size):
            for c in range(grid_size):
                cx = start_x + (c * cell_size) + (cell_size // 2)
                cy = start_y + (r * cell_size) + (cell_size // 2)
                draw.text((cx, cy), grid[r][c], fill="black", font=font_label, anchor="mm")

    def render_panel_d_icon_scatter(self, canvas, draw, rect, words, distractors):
        draw.text((rect['x'] + rect['w']//2, rect['y'] + 60), "Find the Rhymes", fill="black", font=font_label, anchor="mt")
        items = words + distractors[:7]; random.shuffle(items)
        placed_rects = []; icon_size = 250
        safe_x = rect['x'] + 100; safe_y = rect['y'] + 200; safe_w = rect['w'] - 200; safe_h = rect['h'] - 250
        for item in items:
            placed = False; attempts = 0
            while not placed and attempts < 50:
                rx = random.randint(safe_x, safe_x + safe_w - icon_size)
                ry = random.randint(safe_y, safe_y + safe_h - icon_size)
                if not any(rx < pr[2] and rx+icon_size > pr[0] and ry < pr[3] and ry+icon_size > pr[1] for pr in placed_rects):
                    ic = get_icon_image(item)
                    if ic:
                        paste_centered(canvas, ic, rx + icon_size//2, ry + icon_size//2, icon_size)
                        placed_rects.append((rx, ry, rx+icon_size, ry+icon_size))
                        placed = True
                attempts += 1

    def render_panel_e_checklist(self, canvas, draw, rect, words):
        draw.text((rect['x'] + rect['w']//2, rect['y'] + 60), "Checklist", fill="black", font=font_label, anchor="mt")
        start_y = rect['y'] + 250; gap = 150
        tasks = [f"Find {w}" for w in words] + ["Count them all", "Check the spelling"]
        for i, task in enumerate(tasks):
            y_pos = start_y + (i * gap)
            draw.rectangle([rect['x'] + 150, y_pos, rect['x'] + 210, y_pos + 60], outline="black", width=4)
            draw.text((rect['x'] + 250, y_pos + 10), task, fill="black", font=font_instr, anchor="lt")
         # Assuming logic not needed since we are removing classic check per user request for final output replacement?
         # User said: "search for if variant == 'Classic': and delete those lines so Sheet 2 generates."
         # And: "look at this code and edit it to ensure that the formatting, placements, fonts, icons, dimensions of elements all match what you have done so far."
         # User provided a block of code in the prompt which is NEW code? Or existing code?
         # The code in the prompt seems to be the logic for S2 generation.
         # Ah, the user provided CODE in the prompt they want me to ADOPT/MERGE.
         # AND REMOVE the 'if variant == Classic' check.
         # Wait, looking at the user's prompt code... it HAS 'render_header_s1' logic but DIFFERENT coordinates.
         # User's code prompt TITLE x:280, y:210. My code has x:250 y:120.
         
         # The user provided a FULL FILE CONTENT in the prompt block.
         # They want me to use THAT code but ensure it matches "what I have done so far" (my fixes).
         # My fixes: Height of Panel C (1350), Overlay ordering fix, S1 instruction Logic fix.
         # The User's prompt code HAS the Panel C 1350 fix comment. HAS the S1-A/B/C/D logic.
         # BUT it has different Header coordinates?
         # And it has `render_header_s2`, which matches my S1 logic?
         
         # The user says: "search for if variant == 'Classic': and delete those lines so Sheet 2 generates."
         # In the prompt code, `generate_sheet_2` has:
         # if variant == 'S2-A': ... elif variant == 'S2-B': ... else: # CLASSIC MODE
         
         # If I delete `else` (Classic), then if `variant` is neither, nothing happens?
         # "delete those lines so Sheet 2 generates."
         # Maybe they mean: Force S2 to always generate? OR remove the constraint preventing it?
         # Actually, the prompt code has:
         # if variant == 'S2-A': ... elif variant == 'S2-B': ... else: # Classic logic.
         
         # If I delete `if variant == 'Classic'`, maybe they mean the check in a loop?
         # But in `generate_sheet_2`, logic handles Classic in `else`.
         
         # Wait! "search for if variant == 'Classic': and delete those lines".
         # Maybe in the `if __name__ == "__main__":` block which is empty in the prompt?
         # No.
         
         # Let's look at `render_panel_d_classic`...
         
         # Let's look at `generate_sheet_2` in the prompt code.
         # It renders logic for variants.
         
         # I will adopt the user's code, apply my overlay fix (if missing in prompt code), and ensure fonts/paths match.
         
         # Prompt code Overlay Logic:
         # ov_path = ...
         # if exists: try: canvas = Image.alpha_composite(canvas, ov) ...
         # This matches my fix!
         
         # Prompt Code Header S1 Logic:
         # `render_header_s1`: Uses `i_box["x"]` etc. Draws multiline text.
         # My `render_header_s1` does manual line drawing for "Today you'll..."
         # The prompt code attempts to use `multiline_text`? 
         # Wait, the prompt code logic for Instructions:
         # Draws "Today you'll..." manually (Part 1, 2, 3), then Line, then 'body_lines'.
         # This matches my logic.
         
         # Prompt Code Panel C Height: 1350. Matches.
         
         # The user wants me to REMOVE `if variant == 'Classic'`.
         # The code has `variant = quest.get('variant_s2', 'Classic')`.
         # Then `if variant == 'S2-A': ... elif ... else:`.
         # If I remove the check, how does it handle defaults?
         # "delete those lines so Sheet 2 generates" -> Maybe they imply existing code blocked Classic?
         # Or they want Classic to be the `else` block and just run?
         
         # I think the user is providing a new script and wants me to save it, but REMOVE some block they dislike.
         # I will just write the provided code to `modular_factory.py`, ensuring `generate_sheet_2` works.
         # I will ensure `if __name__` block runs the generation.
         
    pass

    def generate_sheet_2(self, quest):
        print(f"Generating Modular S2: {quest['name']}")
        canvas = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # GREEN BORDERS & UNLOCKED CLASSIC
        for k in ["D", "E"]:
            p = LAYOUT["S2_PANELS"][k]
            draw.rounded_rectangle([p['x'], p['y'], p['x']+p['w'], p['y']+p['h']], radius=60, outline=COLOR_GREEN, width=25)

        distractors = self.get_distractors(10, exclude=quest['words'])
        variant = quest.get('variant_s2', 'Classic')
        
        if variant == 'S2-A':
            self.render_panel_d_riddles(canvas, draw, LAYOUT["S2_PANELS"]["D"], quest['words'], distractors)
            self.render_panel_e_wordsearch(canvas, draw, LAYOUT["S2_PANELS"]["E"], quest['words'])
        elif variant == 'S2-B':
            self.render_panel_d_icon_scatter(canvas, draw, LAYOUT["S2_PANELS"]["D"], quest['words'], distractors)
            self.render_panel_e_checklist(canvas, draw, LAYOUT["S2_PANELS"]["E"], quest['words'])
        else:
            # CLASSIC MODE - Manually Rendered Sorting Mats
            # Panel D: Target Family
            rect_d = LAYOUT["S2_PANELS"]["D"]
            draw.text((rect_d['x'] + rect_d['w']//2, rect_d['y'] + 50), "Words ending in", fill="black", font=font_label, anchor="mt")
            draw.text((rect_d['x'] + rect_d['w']//2, rect_d['y'] + 180), f"-{quest['target']}", fill=COLOR_GREEN, font=font_family, anchor="mt")
            
            # Panel E: Other Words
            rect_e = LAYOUT["S2_PANELS"]["E"]
            draw.text((rect_e['x'] + rect_e['w']//2, rect_e['y'] + 50), "Other Words", fill="black", font=font_label, anchor="mt")

        ov_path = os.path.join(OVERLAYS_DIR, f"overlay_{quest['id']}.png")
        if os.path.exists(ov_path):
             try:
                ov = Image.open(ov_path).convert("RGBA").resize((WIDTH, HEIGHT))
                canvas = Image.alpha_composite(canvas, ov)
             except Exception: pass

        draw = ImageDraw.Draw(canvas)
        self.render_header_s2(draw, quest)
        
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
        canvas.save(os.path.join(OUTPUT_DIR, f"{quest['id']}_Sheet2_Modular.png"))

if __name__ == "__main__":
    if os.path.exists("project_state.json"):
        factory = WorksheetFactory("project_state.json")
        for q in factory.syllabus:
            try:
                factory.generate_sheet_1(q)
                factory.generate_sheet_2(q)
            except Exception as e:
                print(f"Error {q['id']}: {e}")
