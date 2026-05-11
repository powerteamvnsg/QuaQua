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
from src.agents.curriculum_architect import CurriculumArchitect, SpecValidationError
from src.agents.quality_agent import QualityStandardsAgent
from src.agents.worksheet_generator import WorksheetGenerator
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
        """
        Execute the full pipeline. Returns path to final PDF.

        Each step is inspected before proceeding to the next.
        """
        self._log("=" * 60)
        self._log(f"WORKSHEET PIPELINE — {self.topic} / {self.theme_name}")
        self._log("=" * 60)

        # ── Step 1 ── Build the curriculum blueprint
        self._log("\n📋 STEP 1: Building curriculum spec...")
        self.spec = self._step_1_curriculum()
        self._log(f"   ✅ Spec built:\n{self.spec.summary()}")

        # ── Step 2 ── Quality validation
        self._log("\n🔍 STEP 2: Quality validation...")
        self._step_2_quality_check()
        self._log(f"   ✅ QA verdict: {self.spec.qa_verdict}")

        # ── Step 3 ── Enrich with render-ready content
        self._log("\n🔧 STEP 3: Enriching activities for rendering...")
        self._step_3_enrich()
        self._log("   ✅ Activities enriched with render hints")

        # ── Step 4 ── Generate frame art
        self._log("\n🎨 STEP 4: Generating frame art...")
        self._step_4_generate_art()
        self._log("   ✅ Frame art generated")

        # ── Step 5 ── Render activity panels
        self._log("\n📐 STEP 5: Rendering activity panels...")
        self._step_5_render_panels()
        self._log("   ✅ Panels rendered")

        # ── Step 6 ── Composite overlays
        self._log("\n🖼️  STEP 6: Compositing overlays...")
        self._step_6_composite()
        self._log("   ✅ Overlays composited")

        # ── Step 7 ── Final QA
        self._log("\n🏁 STEP 7: Final QA review...")
        self._step_7_critic()
        self._log(f"   ✅ Critic verdict: {self.spec.critic_verdict}")

        # ── Step 8 ── Bind PDF
        self._log("\n📕 STEP 8: Binding PDF...")
        pdf_path = self._step_8_bind()
        self._log(f"   ✅ PDF: {pdf_path}")

        self._log("\n" + "=" * 60)
        self._log("PIPELINE COMPLETE")
        self._log("=" * 60)

        return pdf_path

    # ──────────────────────────────────────────────────────────
    # STEP IMPLEMENTATIONS
    # ──────────────────────────────────────────────────────────

    def _step_1_curriculum(self) -> BundleSpec:
        """Delegate to CurriculumArchitect and inspect result."""
        spec = CurriculumArchitect.build_spec(self.topic, self.theme)

        # Orchestrator inspection: verify the blueprint matches vision
        assert len(spec.sheets) == 4, f"Expected 4 sheets, got {len(spec.sheets)}"
        expected_panels = [3, 3, 2, 1]
        for sheet, expected in zip(spec.sheets, expected_panels):
            assert sheet.panel_count == expected, (
                f"Sheet {sheet.sheet_number}: expected {expected} panels, "
                f"got {sheet.panel_count}"
            )
            assert len(sheet.activities) == expected, (
                f"Sheet {sheet.sheet_number}: expected {expected} activities, "
                f"got {len(sheet.activities)}"
            )

        return spec

    def _step_2_quality_check(self) -> None:
        """Delegate to QualityStandardsAgent and inspect result."""
        verdict = QualityStandardsAgent.verify(self.spec)
        self.spec.qa_verdict = verdict.to_dict()

        if verdict.release_blocked:
            self._log(f"   ❌ QA FAILED — Pipeline blocked")
            for d in verdict.defects:
                self._log(f"      {d}")
            raise RuntimeError(
                f"Quality check failed with {len(verdict.defects)} defects. "
                f"Pipeline blocked."
            )

    def _step_3_enrich(self) -> None:
        """Delegate to WorksheetGenerator for render enrichment."""
        WorksheetGenerator.generate(self.spec)

        # Orchestrator inspection: verify _render hints exist
        for sheet in self.spec.sheets:
            for act in sheet.activities:
                assert "_render" in act.content, (
                    f"Sheet {sheet.sheet_number}, '{act.activity_type}': "
                    f"missing _render hints after enrichment"
                )

    def _step_4_generate_art(self) -> None:
        """
        Generate themed frame art for each sheet.

        In a live environment, this would call the generate_image tool.
        Here, we create placeholder PNGs and record the paths so the
        pipeline can be tested end-to-end.
        """
        from PIL import Image, ImageDraw, ImageFont

        for sheet in self.spec.sheets:
            sheet_art = {}
            components = ["character_scene", "bottom_frame", "right_frame"]
            sizes = {
                "character_scene": (762, 717),
                "bottom_frame": (2751, 265),
                "right_frame": (270, 1776),
            }

            for comp in components:
                w, h = sizes[comp]
                # Create a placeholder image with label
                img = Image.new("RGBA", (w, h), (245, 245, 220, 200))
                draw = ImageDraw.Draw(img)
                label = f"Sheet {sheet.sheet_number}\n{comp}\n{sheet.story_beat}"
                try:
                    font = ImageFont.load_default()
                except Exception:
                    font = None
                draw.text((10, 10), label, fill=(100, 100, 100), font=font)

                path = self.art_dir / f"sheet{sheet.sheet_number}_{comp}.png"
                img.save(str(path))
                sheet_art[comp] = str(path)

            sheet.frame_art_paths = sheet_art

    def _step_5_render_panels(self) -> None:
        """
        Render activity panels onto A4 canvases.

        Creates a white A4 canvas with bordered panels for each sheet.
        In a full implementation, this delegates to modular_factory.py's
        WorksheetFactory. For now, creates structured placeholders.
        """
        from PIL import Image, ImageDraw, ImageFont

        for sheet in self.spec.sheets:
            canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
            draw = ImageDraw.Draw(canvas)

            # Draw panel borders based on panel_count
            self._draw_panels(draw, sheet)

            path = self.panels_dir / f"Worksheet_Q{sheet.sheet_number:02d}.png"
            canvas.save(str(path))
            sheet.rendered_panel_path = str(path)

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

    def _draw_panels(self, draw, sheet: SheetSpec) -> None:
        """Draw bordered activity panels on the canvas."""
        from PIL import ImageFont

        # Panel area (below header zone)
        panel_top = 600
        panel_left = 150
        panel_right = 3200
        panel_bottom = 2200
        panel_width = panel_right - panel_left
        panel_height = panel_bottom - panel_top
        gap = 40

        n = sheet.panel_count
        if n == 3:
            w = (panel_width - gap * 2) // 3
            rects = [
                (panel_left, panel_top, panel_left + w, panel_bottom),
                (panel_left + w + gap, panel_top, panel_left + 2*w + gap, panel_bottom),
                (panel_left + 2*w + 2*gap, panel_top, panel_right, panel_bottom),
            ]
        elif n == 2:
            w = (panel_width - gap) // 2
            rects = [
                (panel_left, panel_top, panel_left + w, panel_bottom),
                (panel_left + w + gap, panel_top, panel_right, panel_bottom),
            ]
        else:  # n == 1
            rects = [(panel_left, panel_top, panel_right, panel_bottom)]

        # Draw each panel with rounded corners and activity label
        for i, rect in enumerate(rects):
            draw.rounded_rectangle(rect, radius=20, outline=(180, 30, 30), width=3)

            # Label with activity type
            if i < len(sheet.activities):
                act = sheet.activities[i]
                label = f"{act.activity_type}\n{act.instructions[:40]}..."
                try:
                    font = ImageFont.load_default()
                except Exception:
                    font = None
                draw.text(
                    (rect[0] + 20, rect[1] + 20),
                    label,
                    fill=(100, 100, 100),
                    font=font,
                )

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
