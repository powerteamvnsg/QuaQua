from PIL import Image
import numpy as np

def visualize_alpha(path):
    img = Image.open(path)
    alpha = np.array(img)[:, :, 3]
    h, w = alpha.shape
    
    # 20x20 grid
    rows, cols = 20, 40
    rh, rw = h // rows, w // cols
    
    grid = ""
    for r in range(rows):
        for c in range(cols):
            block = alpha[r*rh:(r+1)*rh, c*rw:(c+1)*rw]
            if np.any(block > 0):
                grid += "X"
            else:
                grid += "."
        grid += "\n"
    print(f"Alpha Map for {path}:")
    print(grid)

visualize_alpha("data/assets/frames/temp_verify/grid02_01.png")
