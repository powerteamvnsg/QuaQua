"""
Worksheet Pipeline Orchestrator — The Project Manager.

Holds the vision of the final 4-sheet lesson bundle and delegates to
specialist agents, inspecting each deliverable before proceeding.

Usage:
    python worksheet_pipeline.py --topic at_family --theme pirate
    python worksheet_pipeline.py --topic beginning_sounds --theme space
"""

from __future__ import annotations
import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    PROJECT_ROOT as CFG_ROOT,
    OUTPUT_DIR, FINAL_PRODUCTION_DIR,
    OVERLAY_THEMES_PATH, OVERLAY_SCHEMA_PATH,
    A4_WIDTH, A4_HEIGHT,
)
from src.models.worksheet_spec import (
    ActivitySpec, SheetSpec, ThemeSpec, BundleSpec,
)
from src.engines.curriculum.curriculum_architect import CurriculumArchitect, SpecValidationError
from src.agents.quality_agent import QualityStandardsAgent
from src.engines.lesson.worksheet_generator import WorksheetGenerator
from src.agents.critic_agent import CriticAgent


# ============================================================
# THEME LOADER
# ============================================================

def load_theme(theme_name: str) -> ThemeSpec:
    """Load a ThemeSpec from config/overlay_themes.json."""
    with open(OVERLAY_THEMES_PATH, "r") as f:
        themes = json.load(f)

    if theme_name not in themes:
        available = list(themes.keys())
        raise ValueError(
            f"Unknown theme '{theme_name}'. Available: {available}"
        )

    raw = themes[theme_name]
    return ThemeSpec(
        name=theme_name,
        style_tokens=raw.get("style_tokens", ""),
        banner_prompt=raw.get("banner_prompt", ""),
        mascots=raw.get("mascots", []),
        story_sequence=raw.get("story_sequence", []),
    )


# ============================================================
# THE ORCHESTRATOR
# ============================================================

class WorksheetPipeline:
    """
    The Project Manager.

    Holds the blueprint of the final product and delegates to agents:
    1. CurriculumArchitect  → build curriculum spec (BundleSpec)
    2. QualityStandardsAgent → validate diversity & correctness
    3. WorksheetGenerator    → enrich with render-ready content
    4. Image Generation      → create themed frame art (4 sheets)
    5. Rendering             → draw activity panels via modular_factory
    6. Overlay Compositing   → overlay frames onto worksheets
    7. CriticAgent           → final visual QA
    8. PDF Binding           → combine into single PDF

    At each step, the orchestrator inspects the result before proceeding.
    """

    def __init__(self, topic: str, theme_name: str):
        self.topic = topic
        self.theme_name = theme_name
        self.theme = load_theme(theme_name)
        self.spec: BundleSpec | None = None

        # Output directory for this run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = OUTPUT_DIR / f"run_{topic}_{theme_name}_{timestamp}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # Sub-directories
        self.art_dir = self.run_dir / "frame_art"
        self.panels_dir = self.run_dir / "panels"
        self.overlays_dir = self.run_dir / "overlays"
        self.art_dir.mkdir(exist_ok=True)
        self.panels_dir.mkdir(exist_ok=True)
        self.overlays_dir.mkdir(exist_ok=True)

    def run(self) -> str:
        self._log("=" * 60)
        self._log(f"WORKSHEET PIPELINE — {self.topic} / {self.theme_name}")
        self._log("=" * 60)

        try:
            self._log("\n📋 STEP 1: Building curriculum spec...")
            self._step_1_architect()
            self._log(f"   ✅ Spec built:\n{self.spec.summary()}")

            self._log("\n🔍 STEP 2: Quality validation...")
            self._step_2_qa()
            self._log(f"   ✅ QA verdict: {self.spec.qa_verdict}")

            self._log("\n🔧 STEP 3: Enriching activities for rendering...")
            self._step_3_generator()
            self._log("   ✅ Activities enriched with render hints")

            self._log("\n🎨 STEP 4: Generating frame art...")
            self._step_4_generate_art()
            self._log("   ✅ Frame art generated")

            self._log("\n📐 STEP 5: Rendering activity panels...")
            self._step_5_render_panels()
            self._log("   ✅ Panels rendered")

            self._log("\n🖼️  STEP 6: Compositing overlays...")
            self._step_6_composite()
            self._log("   ✅ Overlays composited")

            self._log("\n🏁 STEP 7: Final QA review...")
            self._step_7_critic()
            self._log(f"   ✅ Critic verdict: {self.spec.critic_verdict}")

            self._log("\n📕 STEP 8: Binding PDF...")
            pdf_path = self._step_8_bind()
            self._log(f"   ✅ PDF: {pdf_path}")

        except Exception as e:
            self._log(f"   ❌ pipeline generation mistakes: {str(e)}")
            raise

        self._log("\n" + "=" * 60)
        self._log("PIPELINE COMPLETE")
        self._log("=" * 60)

        return pdf_path
    def _step_1_architect(self) -> None:
        spec = CurriculumArchitect.build_spec(self.topic, self.theme)
        self.spec = spec

    def _step_2_qa(self) -> None:
        from src.agents.quality_agent import QualityStandardsAgent
        verdict = QualityStandardsAgent.verify(self.spec)
        self.spec.qa_verdict = verdict.to_dict()
        if verdict.release_blocked:
            raise RuntimeError(f"QA failed: {verdict.defects}")

    def _step_3_generator(self) -> None:
        WorksheetGenerator.generate(self.spec)

    def _step_4_generate_art(self) -> None:
        from src.engines.layout.asset_layout_generator import generate_art_placeholders
        generate_art_placeholders(self.spec, self.art_dir)
        self._log('   ✅ Frame art generated by Asset & Layout Generator')

    def _step_5_render_panels(self) -> None:
        from src.engines.layout.asset_layout_generator import render_panels
        render_panels(self.spec, self.panels_dir)
        self._log('   ✅ Panels rendered by Asset & Layout Generator')

    def _step_6_composite(self) -> None:
        """
        Composite frame art overlay onto rendered panels.

        Uses overlay_generator_v2.py's compositing logic.
        """
        from PIL import Image

        for sheet in self.spec.sheets:
            if not sheet.rendered_panel_path:
                continue

            # Load the rendered panel
            base = Image.open(sheet.rendered_panel_path).convert("RGBA")

            # Overlay each frame art piece at its schema position
            positions = {
                "character_scene": (2746, 1763),
                "bottom_frame": (0, 2215),
                "right_frame": (3238, 0),
            }

            for comp, (x, y) in positions.items():
                art_path = sheet.frame_art_paths.get(comp)
                if art_path and os.path.exists(art_path):
                    art = Image.open(art_path).convert("RGBA")
                    base.paste(art, (x, y), art)

            # Save as RGB for PDF compatibility
            output = base.convert("RGB")
            path = self.overlays_dir / f"Worksheet_Q{sheet.sheet_number:02d}.png"
            output.save(str(path))
            sheet.overlay_path = str(path)

    def _step_7_critic(self) -> None:
        """Delegate to CriticAgent for final review."""
        verdict = CriticAgent.review(self.spec)
        self.spec.critic_verdict = verdict

        if verdict["decision"] == "REJECTED":
            self._log("   ⚠️  Critic found issues (non-blocking for now):")
            for issue in verdict.get("issues", []):
                self._log(f"      - {issue}")

    def _step_8_bind(self) -> str:
        """Bind all overlaid worksheets into a single PDF."""
        from PIL import Image

        pages = []
        for sheet in sorted(self.spec.sheets, key=lambda s: s.sheet_number):
            path = sheet.overlay_path or sheet.rendered_panel_path
            if path and os.path.exists(path):
                img = Image.open(path)
                if img.mode == "RGBA":
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                pages.append(img)

        if not pages:
            raise RuntimeError("No pages to bind — pipeline produced no output")

        pdf_path = str(self.run_dir / f"K2_{self.topic}_{self.theme_name}_bundle.pdf")
        pages[0].save(
            pdf_path, "PDF",
            resolution=300.0,
            save_all=True,
            append_images=pages[1:],
        )
        self.spec.pdf_path = pdf_path

        # Also save the spec as JSON for debugging
        spec_path = self.run_dir / "bundle_spec.json"
        self._save_spec_json(spec_path)

        return pdf_path

    # ──────────────────────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────────────────────

    def _save_spec_json(self, path: Path) -> None:
        """Save the BundleSpec as JSON for debugging."""
        from dataclasses import asdict
        data = {
            "subject": self.spec.subject,
            "topic": self.spec.topic,
            "theme": self.spec.theme.name,
            "qa_verdict": self.spec.qa_verdict,
            "critic_verdict": self.spec.critic_verdict,
            "pdf_path": self.spec.pdf_path,
            "sheets": [],
        }
        for s in self.spec.sheets:
            sheet_data = {
                "sheet_number": s.sheet_number,
                "panel_count": s.panel_count,
                "difficulty": s.difficulty,
                "story_beat": s.story_beat,
                "rendered_panel_path": s.rendered_panel_path,
                "overlay_path": s.overlay_path,
                "activities": [
                    {
                        "type": a.activity_type,
                        "instructions": a.instructions,
                        "content_keys": list(a.content.keys()),
                    }
                    for a in s.activities
                ],
            }
            data["sheets"].append(sheet_data)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _log(self, msg: str) -> None:
        """Print a log message."""
        print(msg)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="K2 Worksheet Pipeline — Generate a 4-sheet lesson bundle"
    )
    parser.add_argument(
        "--topic", required=True,
        help="Curriculum topic key (e.g. at_family, beginning_sounds)"
    )
    parser.add_argument(
        "--theme", required=True,
        help="Visual theme name (e.g. pirate, space)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Build spec and validate without rendering"
    )
    args = parser.parse_args()

    pipeline = WorksheetPipeline(topic=args.topic, theme_name=args.theme)

    if args.dry_run:
        # Just build and validate the spec
        spec = CurriculumArchitect.build_spec(args.topic, pipeline.theme)
        WorksheetGenerator.generate(spec)
        verdict = QualityStandardsAgent.verify(spec)
        print(f"\n{spec.summary()}")
        print(f"\nQA Verdict: {verdict}")
        return

    pdf_path = pipeline.run()
    print(f"\n🎉 Done! PDF at: {pdf_path}")


if __name__ == "__main__":
    main()
