from PIL import Image
import os
import numpy as np

def audit_fixed_frame(path):
    img = Image.open(path)
    if img.mode != 'RGBA':
        print(f"FAILED: {path} is not RGBA.")
        return
    
    data = np.array(img)
    alpha = data[:, :, 3]
    w, h = img.size
    
    # Check "Safe Zone" (center-left)
    # User specified 257mm x 175mm
    ws_w = int(257 / 25.4 * 300)
    ws_h = int(175 / 25.4 * 300)
    
    # Margin calculation: center vertically, aligned to some offset?
    # Usually this means the content box. Let's check the top-left portion.
    check_area = alpha[0:ws_h, 0:ws_w]
    non_transparent = np.count_nonzero(check_area)
    
    print(f"Audit for {path}:")
    print(f" - Non-transparent pixels in {ws_w}x{ws_h} safe zone: {non_transparent}")
    
    if non_transparent == 0:
        print(" - RESULT: PASSED (100% Transparent Workspace)")
    else:
        # If it's not 100%, let's see where the pixels are.
        print(f" - RESULT: FAILED (Margin Violation - {non_transparent} pixels found)")

paths = [
    "data/assets/frames/temp_verify/grid02_01.png",
    "data/assets/frames/temp_verify/grid02_06.png",
    "data/assets/frames/temp_verify/grid02_10.png"
]

for p in paths:
    if os.path.exists(p):
        audit_fixed_frame(p)
    else:
        print(f"NOT FOUND: {p}")
