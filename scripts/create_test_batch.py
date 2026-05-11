
import cv2
import numpy as np
import os

# Define paths
output_dir = r"D:\moetvnpapers\k2-worksheet-generator\data\assets\imagesforiconcrop"
output_path = os.path.join(output_dir, "space_batch_test.png")

# Ensure directory exists
os.makedirs(output_dir, exist_ok=True)

# Create a TRANSPARENT canvas (RGBA) -> Zeros
width, height = 2500, 1500
img = np.zeros((height, width, 4), dtype=np.uint8)

# Define 10 positions (2 rows of 5)
rows = [400, 1100]
cols = [250, 750, 1250, 1750, 2250]

count = 0
for r_idx, cy in enumerate(rows):
    for c_idx, cx in enumerate(cols):
        # Draw a colored circle (content) with Alpha 255
        # Color: Black (0,0,0) opaque
        cv2.circle(img, (cx, cy), 150, (0, 0, 0, 255), -1)
        
        # Add text
        cv2.putText(img, f"{count+1}", (cx-50, cy+50), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255, 255), 5)
        count += 1

# Save
cv2.imwrite(output_path, img)
print(f"Created transparent test batch image at: {output_path}")
