
import cv2
import numpy as np
import os
from pathlib import Path

def standardize_image(img, size=(512, 512), padding_pct=0.1):
    """Tight crop -> padding -> resize."""
    if img is None:
        return None
    
    # 1. Get Alpha Mask or fallback to Grayscale for content detection
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

    # 2. Find ROI
    coords = cv2.findNonZero(alpha)
    if coords is None:
        return None
    x, y, w, h = cv2.boundingRect(coords)
    roi = img[y:y+h, x:x+w]

    # 3. Square padding
    max_dim = max(w, h)
    pad_px = int(max_dim * padding_pct)
    total_dim = max_dim + (2 * pad_px)
    
    new_img = np.zeros((total_dim, total_dim, 4), dtype=np.uint8)
    
    # Center ROI
    off_x = (total_dim - w) // 2
    off_y = (total_dim - h) // 2
    
    if roi.shape[2] == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2BGRA)
    
    new_img[off_y:off_y+h, off_x:off_x+w] = roi
    
    # 4. Final Resize
    final = cv2.resize(new_img, size, interpolation=cv2.INTER_LANCZOS4)
    return final

def extract_sheet(sheet_path, labels_grid, output_dir):
    print(f"Processing {sheet_path}...")
    img = cv2.imread(str(sheet_path), cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"Error: Could not load {sheet_path}")
        return

    # Create alpha if missing
    if img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        img[:, :, 3] = alpha

    # Aggressive threshold for contour detection
    _, alpha_thresh = cv2.threshold(img[:, :, 3], 100, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    alpha_thresh = cv2.morphologyEx(alpha_thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(alpha_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 100 and h > 100 and w < img.shape[1] * 0.9:
            valid_contours.append((x, y, w, h))
    
    # Sort into rows
    valid_contours.sort(key=lambda b: b[1])
    rows = []
    if valid_contours:
        current_row = [valid_contours[0]]
        for i in range(1, len(valid_contours)):
            if valid_contours[i][1] < current_row[-1][1] + 200: # Larger gap for rows
                current_row.append(valid_contours[i])
            else:
                rows.append(sorted(current_row, key=lambda b: b[0]))
                current_row = [valid_contours[i]]
        rows.append(sorted(current_row, key=lambda b: b[0]))

    print(f"Found {len(rows)} rows.")
    for r_idx, row in enumerate(rows):
        print(f"  Row {r_idx}: {len(row)} items")
        if r_idx < len(labels_grid):
            for c_idx, (x, y, w, h) in enumerate(row):
                if c_idx < len(labels_grid[r_idx]):
                    label = labels_grid[r_idx][c_idx]
                    if not label: continue
                    
                    roi = img[y:y+h, x:x+w]
                    final = standardize_image(roi)
                    if final is not None:
                        out_path = output_dir / f"{label}.png"
                        cv2.imwrite(str(out_path), final)
                        print(f"  Saved: {out_path}")

# Config
REF_DIR = Path(r"D:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\Library\Characters\references")
OUT_DIR = Path(r"D:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\Library\Characters")

SHEETS = {
    "Gemini_Generated_Image_1evoss1evoss1evo (1).png": [
        ["ref_strawberry_queen", "ref_pineapple_scholar", "ref_carrot_gardener", "ref_turnip_lady", "ref_broccoli_gentleman", "ref_cherries"],
        ["ref_pea_baby", "ref_corn_hero", "ref_lemon_student", "ref_watermelon_doctor", "ref_pineapple_graduate", "ref_cucumber_cool"],
        ["ref_beet_hip", "ref_apple_artist", "ref_tomato_chef", "ref_grape_lantern", "ref_watermelon_formal", "ref_onion_police"],
        ["ref_garlic_gardener", "ref_peach_writer", "ref_spinach_sailor", "ref_mango_fairy", "ref_bean_detective", "ref_asparagus_soldier"],
        ["ref_fig_fireman", "ref_plum_aviator", "ref_cauliflower_chef", "ref_potato_scientist", "ref_blueberry_ballerina", "ref_mangosteen_musician"]
    ],
    "jj9jtxjj9jtxjj9j.png": [
        ["ref_mango_baseball", "ref_fig_fireman_sitting", "ref_pineapple_running"],
        ["ref_strawberry_digging", "ref_turnip_cutting", "ref_asparagus_muscle"],
        ["ref_potato_plumber", "ref_carrot_mixer"]
    ],
    "y4kgmby4kgmby4kg.png": [
        ["ref_mango_baseball_v2", "ref_peach_sitting", "ref_pineapple_running_v2", "ref_strawberry_digging_v2"],
        # Rows 2-5 are likely identical to Sheet 1, so we skip them or name them v2
    ]
}

for filename, grid in SHEETS.items():
    extract_sheet(REF_DIR / filename, grid, OUT_DIR)

# Copy Pirate versions
import shutil
PIRATE_ASSETS = Path(r"D:\AntiGravity Projects\k2-worksheet-generator\output\pirate_assets")
shutil.copy(PIRATE_ASSETS / "tomato.png", OUT_DIR / "ref_tomato_pirate.png")
shutil.copy(PIRATE_ASSETS / "blueberry.png", OUT_DIR / "ref_blueberry_pirate.png")
print("Copied pirate versions.")

# Special case for ref_tomato.png (The user specifically asked for this)
# We'll use the tomato_chef as a base or maybe there's a better one.
# Let's just use tomato_chef as ref_tomato for now as requested.
shutil.copy(OUT_DIR / "ref_tomato_chef.png", OUT_DIR / "ref_tomato.png")
print("Created ref_tomato.png from ref_tomato_chef.png")
