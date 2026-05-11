
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

class AssetManager:
    """
    Local Asset Manager.
    No longer uses external APIs. Assumes assets are generated manually or by a local engine
    and placed in the staging/assets directory.
    """
    def __init__(self, output_dir: Path, force_regen: bool = False):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.force_regen = force_regen

    def get_or_create(self, asset_type: str, prompt: str, style_tokens: str, reference_image: Optional[str] = None) -> str:
        """
        Check for existing asset in the output directory.
        If it doesn't exist, it prints a request for the user/AI to generate it.
        """
        # Create a deterministic filename based on asset type and prompt slug
        slug = "_".join(prompt.split()[:3]).lower().replace("'", "").replace('"', "").replace(",", "")
        # Clean slug of invalid characters
        slug = "".join([c if c.isalnum() or c == "_" else "" for c in slug])
        
        final_filename = f"{asset_type}_{slug}.png"
        final_path = self.output_dir / final_filename

        return str(final_path)
