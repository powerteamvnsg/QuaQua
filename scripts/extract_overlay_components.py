"""
Extract fixed components (instruction box + portrait) from existing overlays.
These components are reused across all themed overlays.
"""
import os
from PIL import Image

# Configuration
OVERLAY_SOURCE = r"d:\moetvnpapers\k2-worksheet-generator\data\assets\overlays\overlay_Q01.png"
OUTPUT_DIR = r"d:\moetvnpapers\k2-worksheet-generator\data\assets\overlay_components"

# Component bounding boxes (x, y, width, height) - based on 3508x2480 canvas
COMPONENTS = {
    "instruction_box": {
        "bbox": (1650, 120, 2970, 320),  # Top-right instruction box
        "description": "Blue-bordered instruction box"
    },
    "portrait_strawberry": {
        "bbox": (2800, 180, 3100, 480),  # Circular strawberry mascot portrait
        "description": "Strawberry King mascot portrait circle"
    },
    "instruction_with_portrait": {
        "bbox": (1650, 120, 3100, 480),  # Combined instruction box + portrait
        "description": "Instruction box with attached portrait"
    }
}

def extract_components():
    """Extract fixed overlay components from source image."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load source overlay
    print(f"Loading source overlay: {OVERLAY_SOURCE}")
    source = Image.open(OVERLAY_SOURCE).convert("RGBA")
    print(f"Source dimensions: {source.size}")
    
    # Extract each component
    for name, config in COMPONENTS.items():
        bbox = config["bbox"]
        print(f"\nExtracting '{name}'...")
        print(f"  Bounding box: {bbox}")
        
        # Crop the region
        component = source.crop(bbox)
        
        # Save as PNG with transparency
        output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        component.save(output_path, "PNG")
        print(f"  Saved to: {output_path}")
        print(f"  Dimensions: {component.size}")
    
    print("\n✅ Component extraction complete!")
    return True

if __name__ == "__main__":
    extract_components()
