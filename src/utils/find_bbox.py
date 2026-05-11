from PIL import Image
import numpy as np
import os

def find_bbox(path):
    img = Image.open(path)
    if img.mode != 'RGBA':
        print(f"{path}: Not RGBA")
        return
    data = np.array(img)
    alpha = data[:, :, 3]
    coords = np.argwhere(alpha > 0)
    if coords.size == 0:
        print(f"{path}: All transparent")
        return
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    print(f"{path}: Content BBox (y_min={y_min}, x_min={x_min}, y_max={y_max}, x_max={x_max})")
    print(f"  Width: {x_max - x_min}, Height: {y_max - y_min}")

paths = [
    "data/assets/frames/temp_verify/grid02_01.png",
    "data/assets/frames/temp_verify/grid02_06.png",
    "data/assets/frames/temp_verify/grid02_10.png"
]

for p in paths:
    if os.path.exists(p):
        find_bbox(p)
