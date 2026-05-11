
import os
import cv2
import numpy as np
import glob
from pathlib import Path

# Directories
DIRS = [
    r"d:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\imagesforiconcrop",
    r"d:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\mascots",
    r"d:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\objects"
]
DEST_DIR = r"d:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\Library"

def get_clean_name(filename):
    # Remove file extension
    base = os.path.splitext(filename)[0]
    # If it's a generated hash (starts with Gemini_Generated...), maybe shorten it?
    # But usually we just keep it or use a prefix.
    # We will just sanitize it.
    return "".join([c for c in base if c.isalnum() or c in (' ', '_', '-')]).strip()

def process_images():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"Created destination directory: {DEST_DIR}")
        
    total_extracted = 0
    
    for d in DIRS:
        if not os.path.exists(d):
            print(f"Directory not found: {d}")
            continue
            
        print(f"Scanning directory: {d}")
        # Case insensitive search for png/jpg
        files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG']:
            files.extend(glob.glob(os.path.join(d, ext)))
            
        folder_name = os.path.basename(d)
        
        for filepath in files:
            print(f"Processing: {os.path.basename(filepath)}")
            clean_fname = get_clean_name(os.path.basename(filepath))
            
            # Read image with alpha channel
            img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"  Failed to load image: {filepath}")
                continue
                
            # Handle standard RGB images by adding alpha channel
            if len(img.shape) == 2: # Gray
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)
            elif img.shape[2] == 3: # BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            
            # Detect objects
            # 1. Create a mask for content vs background
            # Assumption: Background is likely the most frequent color on the border or white/transparent
            
            # Check if alpha channel has transparency already
            has_transparency = False
            if img.shape[2] == 4:
                alpha = img[:, :, 3]
                if np.min(alpha) < 255:
                    has_transparency = True
            
            # Create a binary map of "content"
            if has_transparency:
                # Use alpha channel > threshold as content
                _, thresh = cv2.threshold(img[:, :, 3], 10, 255, cv2.THRESH_BINARY)
            else:
                # Assume white background
                gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                # Invert because usually objects are darker than white background, 
                # but if we just check difference from white:
                # Diff from white (255)
                diff = 255 - gray
                _, thresh = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)
            
            # Clean up noise with morphological operations
            kernel = np.ones((5,5), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=1)
            thresh = cv2.erode(thresh, kernel, iterations=1)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            count = 0
            for i, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                if area < 500: # Skip small noise
                    continue
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Add padding
                pad = 5
                frames_h, frames_w = img.shape[:2]
                x1 = max(0, x - pad)
                y1 = max(0, y - pad)
                x2 = min(frames_w, x + w + pad)
                y2 = min(frames_h, y + h + pad)
                
                crop = img[y1:y2, x1:x2].copy()
                
                # Make background transparent in crop (if it wasn't already)
                # If the original image had no transparency, we now have a crop with white background.
                # We want to make the "semantically background" pixels transparent.
                # Simple approach: Make near-white pixels transparent.
                if not has_transparency:
                    # Convert to HSV to better detect white? Or just RGB.
                    # RGB check:
                    lower = np.array([240, 240, 240, 0])
                    upper = np.array([255, 255, 255, 255])
                    mask = cv2.inRange(crop, lower, upper)
                    crop[mask > 0] = [0, 0, 0, 0] # Set to transparent
                
                # Trim transparent edges (loose crop -> tight crop)
                # Re-check updated alpha
                alpha_c = crop[:, :, 3]
                coords = cv2.findNonZero(alpha_c)
                if coords is not None:
                    x, y, w, h = cv2.boundingRect(coords)
                    crop = crop[y:y+h, x:x+w]
                
                # Save
                # Naming convention: {folder_category}_{filename_part}_{index}.png
                # If filename is generic "New Project", maybe just use folder category?
                # User asked to name by "character and or object name".
                # We can't know that, so we use the safest bet: filename.
                
                # Ensure filename isn't too long
                base_name_part = clean_fname[:30]
                
                save_name = f"{folder_name}_{base_name_part}_item_{count}.png"
                save_path = os.path.join(DEST_DIR, save_name)
                
                cv2.imwrite(save_path, crop)
                count += 1
                total_extracted += 1
                
            print(f"  Extracted {count} objects from {filepath}")

    print("="*40)
    print(f"Processing Complete. Total objects extracted: {total_extracted}")
    print(f"Saved to: {DEST_DIR}")

if __name__ == "__main__":
    process_images()
