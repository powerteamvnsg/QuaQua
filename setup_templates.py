import os
import shutil
from PIL import Image, ImageDraw, ImageFont

# CONFIGURATION
PROJECT_ROOT = os.getcwd()
SOURCE_OVERLAY = os.path.join(PROJECT_ROOT, "data", "assets", "overlays", "Pot of Gold Quest.png")
DEST_SHEET_1 = os.path.join(PROJECT_ROOT, "Pot of Gold Quest.png")
DEST_SHEET_2 = os.path.join(PROJECT_ROOT, "Pot of Gold Quest2.png")

CANVAS_SIZE = (3508, 2480) # A4 Landscape
BG_COLOR = (255, 255, 255)

def create_placeholder(filename, text):
    """Creates a simple placeholder template if missing."""
    print(f"   🎨 Creating placeholder: {filename}...")
    img = Image.new('RGB', CANVAS_SIZE, color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw border
    draw.rectangle([50, 50, CANVAS_SIZE[0]-50, CANVAS_SIZE[1]-50], outline="black", width=10)
    
    # Draw Text
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
        
    # Center Text (Approximation)
    draw.text((CANVAS_SIZE[0]//2 - 400, CANVAS_SIZE[1]//2), text, fill="black", font=font)
    
    img.save(filename)
    print("      ✅ Saved.")

def main():
    print("--- 🛠️ TEMPLATE SETUP UTILITY ---")
    
    # 1. Handle Sheet 1 (Introduction)
    if os.path.exists(DEST_SHEET_1):
        print(f"✅ Sheet 1 Template found in root: {DEST_SHEET_1}")
    elif os.path.exists(SOURCE_OVERLAY):
        print(f"📦 Copying Sheet 1 from overlays to root...")
        shutil.copy(SOURCE_OVERLAY, DEST_SHEET_1)
        print("   ✅ Copied.")
    else:
        print("⚠️ Sheet 1 Template missing entirely. Creating placeholder.")
        create_placeholder(DEST_SHEET_1, "SHEET 1 TEMPLATE (Placeholder)")

    # 2. Handle Sheet 2 (Practice)
    if os.path.exists(DEST_SHEET_2):
         print(f"✅ Sheet 2 Template found in root: {DEST_SHEET_2}")
    else:
        print("⚠️ Sheet 2 Template missing. Creating placeholder.")
        create_placeholder(DEST_SHEET_2, "SHEET 2 TEMPLATE (Placeholder)")

    print("\n--- ✅ SETUP COMPLETE ---")
    print("You can now run 'python batch_generate_visuals.py'")

if __name__ == "__main__":
    main()
