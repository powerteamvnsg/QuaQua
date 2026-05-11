
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class DraftGenerator:
    """ Generates high-quality placeholder drafts for missing assets. """
    @staticmethod
    def create_placeholder(path: Path, asset_type: str, prompt: str, width: int, height: int):
        img = Image.new('RGBA', (width, height), color=(240, 240, 240, 255))
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([0, 0, width-1, height-1], outline=(100, 100, 100), width=10)
        
        # Text Header
        draw.text((20, 20), f"[MISSING {asset_type.upper()}]", fill=(200, 50, 50))
        
        # Word Wrap Prompt (Simple)
        words = prompt.split()
        lines = []
        for i in range(0, len(words), 8):
            lines.append(" ".join(words[i:i+8]))
        
        y = 100
        for line in lines:
            draw.text((40, y), line, fill="black")
            y += 40
            
        img.save(path)
        print(f"      [DRAFT] Generated placeholder: {path.name}")
