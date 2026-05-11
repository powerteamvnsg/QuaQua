import os
import glob
from PIL import Image
from src.config import FINAL_PRODUCTION_DIR, OUTPUT_DIR

INPUT_DIR = str(FINAL_PRODUCTION_DIR)
OUTPUT_PDF = str(OUTPUT_DIR / "K2_Phonics_Worksheets_Batch.pdf")

def bind_book():
    print(f"Binding book from {INPUT_DIR}...")
    
    # regex Glob for Q01.png, Q02.png etc
    # We avoid *FINAL.png from old runs
    # UPDATED: Look for "Worksheet_Q" files specifically
    files = glob.glob(os.path.join(INPUT_DIR, "Worksheet_Q*.png"))
    files.sort()
    
    if not files:
        print("ERROR: No 'Worksheet_Q*.png' files found.")
        print(f"       Checked folder: {INPUT_DIR}")
        print("       Did the factory run?")
        return

    images = []
    print(f"Found {len(files)} pages.")
    
    for f in files:
        print(f"Adding {os.path.basename(f)}...")
        try:
            img = Image.open(f)
            # PDF requires RGB, not RGBA
            if img.mode == 'RGBA':
                # Create white background for alpha
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3]) # 3 is alpha channel
                img = bg
            elif img.mode != 'RGB':
                img = img.convert("RGB")
            
            images.append(img)
        except Exception as e:
            print(f"Error loading {f}: {e}")

    if images:
        # Save first image and append the rest
        first_page = images[0]
        rest_pages = images[1:]
        
        first_page.save(OUTPUT_PDF, "PDF", resolution=100.0, save_all=True, append_images=rest_pages)
        print(f"\nPDF Successfully generated at:\n{OUTPUT_PDF}")
    else:
        print("No valid images processing.")

if __name__ == "__main__":
    bind_book()
