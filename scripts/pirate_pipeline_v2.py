
import os
import sys
from pathlib import Path
from PIL import Image

# Add root to sys.path
sys.path.append(str(Path(__file__).parent))

from src.agents.pipeline import IllustrationPipeline
from src.agents.critic_agent import CriticAgent
from src.agents.generator_agent import MockGeneratorAgent
from overlay_generator_v2 import OverlayGeneratorV2

# CONFIG
STYLE_TOKEN = "Professional Kawaii illustration. Flat Matte illustration style. Thin black outlines. Small black dot eyes with tiny white reflection dot. Solid white background."
OUTPUT_DIR = "output/pirate_v2"
ASSETS_DIR = "output/pirate_assets"

# Mapping for Mock Agent
MAPPING = {
    "blueberry": os.path.join(ASSETS_DIR, "blueberry_tomato_scene.png"),
    "banner": os.path.join(ASSETS_DIR, "banner_a_rustic_piratethemed.png"),
    "voyage": os.path.join(ASSETS_DIR, "frame_01_voyage_a_kawaii_vector.png"),
    "island": os.path.join(ASSETS_DIR, "frame_02_island_a_kawaii_vector.png"),
    "hunt": os.path.join(ASSETS_DIR, "frame_03_hunt_a_kawaii_vector.png"),
    "reward": os.path.join(ASSETS_DIR, "frame_04_reward_a_kawaii_vector.png")
}

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

class PirateGenerator:
    def __init__(self):
        self.generator = MockGeneratorAgent(mapping=MAPPING)
        self.critic = CriticAgent()
        self.pipeline = IllustrationPipeline(self.generator, self.critic)
        self.overlay_gen = OverlayGeneratorV2()

    def generate_frame(self, variant_name, frame_keywords):
        """
        Generates a specific frame variant.
        """
        print(f"\n🏴‍☠️ [PIPELINE] Generating Pirate Frame Variant: {variant_name}...")
        
        # 1. Generate/Fetch Scene (Same for all)
        scene_prompt = f"A cute Blueberry and Tomato dressed as pirates. {STYLE_TOKEN}"
        scene_path = self.pipeline.generation_loop(scene_prompt)
        
        # 2. Generate/Fetch Banner (Same for all)
        banner_prompt = f"A rustic wooden pirate sign board banner. {STYLE_TOKEN}"
        banner_path = self.pipeline.generation_loop(banner_prompt)
        
        # 3. Generate/Fetch Frame Strips (Specific to variant)
        bottom_prompt = f"A horizontal pirate strip themed as {frame_keywords[0]}. {STYLE_TOKEN}"
        bottom_path = self.pipeline.generation_loop(bottom_prompt)
        
        right_prompt = f"A vertical pirate strip themed as {frame_keywords[1]}. {STYLE_TOKEN}"
        right_path = self.pipeline.generation_loop(right_prompt)
        
        # 4. Assemble
        output_file = os.path.join(OUTPUT_DIR, f"pirate_frame_{variant_name}.png")
        self.overlay_gen.compose_overlay_v2(
            title_banner_path=banner_path,
            character_scene_path=scene_path,
            bottom_frame_path=bottom_path,
            right_frame_path=right_path,
            output_path=output_file
        )
        print(f"✅ [SUCCESS] Frame Variant '{variant_name}' saved to: {output_file}")

    def run(self):
        ensure_dirs()
        
        # Define 4 distinct frame variations
        variants = {
            "01_voyage": ["voyage", "voyage"], # Using voyage asset for both bottom/right
            "02_island": ["island", "island"],
            "03_hunt": ["hunt", "hunt"],
            "04_reward": ["reward", "reward"]
        }
        
        for name, keywords in variants.items():
            self.generate_frame(name, keywords)

if __name__ == "__main__":
    pirate_gen = PirateGenerator()
    pirate_gen.run()
