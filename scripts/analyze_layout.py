
import cv2
import numpy as np
import os

# Config
TARGET_W = 3508
TARGET_H = 2480

PATHS = [
    r"C:/Users/tobia/.gemini/antigravity/brain/7b101b76-3dd9-45e8-b45d-8cce848e9da5/uploaded_image_0_1768815619431.png",
    r"C:/Users/tobia/.gemini/antigravity/brain/7b101b76-3dd9-45e8-b45d-8cce848e9da5/uploaded_image_1_1768815619431.png"
]

def analyze_image(path, label_set):
    print(f"\nAnalyzing: {os.path.basename(path)}")
    img = cv2.imread(path)
    if img is None:
        print("Failed to load image.")
        return

    # Resize to target if necessary to get correct coords directly
    h, w = img.shape[:2]
    if w != TARGET_W or h != TARGET_H:
         print(f"Resizing from {w}x{h} to {TARGET_W}x{TARGET_H} for coordinate extraction.")
         img = cv2.resize(img, (TARGET_W, TARGET_H))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold (Black boxes on white -> Invert)
    # White background = 255. Black boxes = 0.
    # We want black regions.
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 100 and h > 100: # Filter noise
            boxes.append({"x": x, "y": y, "w": w, "h": h, "cx": x + w//2, "cy": y + h//2})

    # Logic to identify Main Blocks
    # Headers are usually at the top (low Y). Panels are lower (high Y).
    
    # Sort by CY
    boxes.sort(key=lambda b: b["cy"])
    
    # Split into rows based on Y gap
    rows = []
    if boxes:
        current_row = [boxes[0]]
        for b in boxes[1:]:
            if abs(b["cy"] - current_row[0]["cy"]) < 200: # Same row threshold
                current_row.append(b)
            else:
                rows.append(current_row)
                current_row = [b]
        rows.append(current_row)

    # Naming logic
    results = {}
    
    for i, row in enumerate(rows):
        # Sort row by CX (Left to Right)
        row.sort(key=lambda b: b["cx"])
        
        if i == 0: # Top Row -> Headers
            if len(row) >= 2:
                # Title is usually Left, Instructions Right based on previous context
                # User image 1: Quest Title (Left), Instructions (Right)
                results["HEADER_TITLE"] = row[0]
                results["HEADER_INSTR"] = row[1]
                print(f"  Found Header Title: {row[0]}")
                print(f"  Found Header Instr: {row[1]}")
            else:
                print("  WARNING: Odd number of header elements found.")
        
        elif i == 1: # Bottom Row -> Panels
            if label_set == "S1": # A, B, C
                labels = ["A", "B", "C"]
                for j, panel in enumerate(row):
                    if j < len(labels):
                        name = labels[j]
                        results[f"PANEL_{name}"] = panel
                        print(f"  Found Panel {name}: {panel}")
            elif label_set == "S2": # D, E
                labels = ["D", "E"]
                for j, panel in enumerate(row):
                    if j < len(labels):
                         name = labels[j]
                         results[f"PANEL_{name}"] = panel
                         print(f"  Found Panel {name}: {panel}")

    return results

print("--- EXTRACTING LAYOUT PREFERENCES ---")
s1_coords = analyze_image(PATHS[0], "S1")
s2_coords = analyze_image(PATHS[1], "S2")
