
import cv2
import numpy as np
import os

PATHS = [
    r"C:/Users/tobia/.gemini/antigravity/brain/7b101b76-3dd9-45e8-b45d-8cce848e9da5/uploaded_image_0_1768815619431.png",
    r"C:/Users/tobia/.gemini/antigravity/brain/7b101b76-3dd9-45e8-b45d-8cce848e9da5/uploaded_image_1_1768815619431.png"
]

TARGET_W, TARGET_H = 3508, 2480

def debug_image(path):
    print(f"\nRAW DUMP: {os.path.basename(path)}")
    img = cv2.imread(path)
    if img is None: return

    # Naive scaling factor
    orig_h, orig_w = img.shape[:2]
    scale_x = TARGET_W / orig_w
    scale_y = TARGET_H / orig_h
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    found = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 20: # looser filter
            # Scale to target
            sx = int(x * scale_x)
            sy = int(y * scale_y)
            sw = int(w * scale_x)
            sh = int(h * scale_y)
            found.append((sx, sy, sw, sh))
    
    # Sort by Y then X
    found.sort(key=lambda b: (b[1] // 100, b[0]))
    
    for i, (x, y, w, h) in enumerate(found):
        print(f"Box {i}: x={x}, y={y}, w={w}, h={h}")

debug_image(PATHS[0])
debug_image(PATHS[1])
