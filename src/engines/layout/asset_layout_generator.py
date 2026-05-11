import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# A4 Dimensions
A4_WIDTH = 3508
A4_HEIGHT = 2480

def generate_art_placeholders(spec, art_dir: Path):
    for sheet in spec.sheets:
        sheet_art = {}
        components = ["character_scene", "bottom_frame", "right_frame"]
        sizes = {
            "character_scene": (762, 717),
            "bottom_frame": (2751, 265),
            "right_frame": (270, 1776),
        }

        for comp in components:
            w, h = sizes[comp]
            img = Image.new("RGBA", (w, h), (245, 245, 220, 200))
            draw = ImageDraw.Draw(img)
            label = f"Sheet {sheet.sheet_number}\n{comp}\n{sheet.story_beat}"
            try:
                font = ImageFont.load_default()
            except:
                font = None
            draw.text((10, 10), label, fill=(100, 100, 100), font=font)

            path = art_dir / f"sheet{sheet.sheet_number}_{comp}.png"
            img.save(str(path))
            sheet_art[comp] = str(path)

        sheet.frame_art_paths = sheet_art

def render_panels(spec, panels_dir: Path):
    for sheet in spec.sheets:
        canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # Panel area
        panel_top = 600
        panel_left = 150
        panel_right = 3200
        panel_bottom = 2200
        panel_width = panel_right - panel_left
        gap = 40

        n = sheet.panel_count
        rects = []
        if n == 3:
            w = (panel_width - gap * 2) // 3
            # Panel C is shortened (1350 height)
            panel_c_height = 1350
            rects = [
                (panel_left, panel_top, panel_left + w, panel_bottom),
                (panel_left + w + gap, panel_top, panel_left + 2*w + gap, panel_bottom),
                (panel_left + 2*w + 2*gap, panel_top, panel_right, panel_top + panel_c_height),
            ]
        elif n == 2:
            w = (panel_width - gap) // 2
            rects = [
                (panel_left, panel_top, panel_left + w, panel_bottom),
                (panel_left + w + gap, panel_top, panel_right, panel_bottom),
            ]
        else:  # n == 1
            rects = [(panel_left, panel_top, panel_right, panel_bottom)]

        # Draw each panel with green borders
        for i, rect in enumerate(rects):
            draw.rounded_rectangle(rect, radius=20, outline=(34, 139, 34), width=10) # COLOR_GREEN

            if i < len(sheet.activities):
                act = sheet.activities[i]
                label = f"{act.activity_type}\n{act.instructions[:40]}..."

                # Render the K1/K2 dummy text (words)
                words = act.content.get("words", [])
                if words:
                     label += f"\nWords: {', '.join(words)}"

                try:
                    font = ImageFont.load_default()
                except:
                    font = None
                draw.text(
                    (rect[0] + 20, rect[1] + 20),
                    label,
                    fill=(100, 100, 100),
                    font=font,
                )

        path = panels_dir / f"Worksheet_Q{sheet.sheet_number:02d}.png"
        canvas.save(str(path))
        sheet.rendered_panel_path = str(path)
