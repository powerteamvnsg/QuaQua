from PIL import Image
import os

def clean_cell(img):
    """
    Numpy-optimized cleaning:
    1. Removes checkerboard pattern.
    2. Masks bottom-center.
    """
    import numpy as np
    img = img.convert("RGBA")
    data = np.array(img)
    
    # Identify grey and white (near 255 and near 200)
    # Thresholds for checkerboard
    grey_mask = (data[:,:,0] > 185) & (data[:,:,0] < 215) & \
                (data[:,:,1] > 185) & (data[:,:,1] < 215) & \
                (data[:,:,2] > 185) & (data[:,:,2] < 215)
    
    white_mask = (data[:,:,0] > 240) & (data[:,:,1] > 240) & (data[:,:,2] > 240)
    
    data[grey_mask | white_mask, 3] = 0
    
    # 2. Mask out the bottom-center "Red Cherry" logo
    w, h, _ = data.shape # Careful: shape is (h, w, c)
    # h = row, w = col
    row_start, row_end = int(h*0.85), h
    col_start, col_end = int(w*0.4), int(w*0.6)
    data[row_start:row_end, col_start:col_end, 3] = 0
    
    return Image.fromarray(data)

def extract_quest_frames(grid_path, output_dir, prefix):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(grid_path).convert("RGBA")
    img_w, img_h = img.size
    
    cols, rows = 4, 3
    # Use float for more precise cropping if needed, then cast to int
    cell_w = img_w / cols
    cell_h = img_h / rows
    
    target_w, target_h = 3508, 2480
    
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c + 1
            left = int(c * cell_w)
            top = int(r * cell_h)
            right = int((c + 1) * cell_w)
            bottom = int((r + 1) * cell_h)
            
            crop = img.crop((left, top, right, bottom))
            
            # 1. CLEAN THE CELL
            crop = clean_cell(crop)
            
            if not crop.getbbox():
                continue

            # 2. PROPORTIONAL RESIZE
            new_h = target_h
            current_w, current_h = crop.size
            new_w = int(current_w * (new_h / current_h))
            resized_crop = crop.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 3. CREATE TRANSPARENT CANVAS
            canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            
            # 4. ANCHOR TO BOTTOM-RIGHT
            paste_x = target_w - new_w
            canvas.paste(resized_crop, (paste_x, 0), resized_crop)
            
            save_name = f"{prefix}_{idx:02d}.png"
            save_path = os.path.join(output_dir, save_name)
            canvas.save(save_path, "PNG")
            print(f"Cleaned & Extracted: {save_path}")

# Run for both cleaned grids
if os.path.exists("data/assets/frames/raw_grids/grid_01_portrait.png"):
    extract_quest_frames("data/assets/frames/raw_grids/grid_01_portrait.png", "data/assets/frames/temp_verify/", "grid01")

if os.path.exists("data/assets/frames/raw_grids/grid_02_landscape.png"):
    extract_quest_frames("data/assets/frames/raw_grids/grid_02_landscape.png", "data/assets/frames/temp_verify/", "grid02")
