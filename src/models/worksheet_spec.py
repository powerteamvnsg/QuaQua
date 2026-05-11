"""
Worksheet Spec — The shared data contract for the entire pipeline.

Every agent reads from and writes to these dataclasses.  The Orchestrator
creates a BundleSpec, passes it through the pipeline, and each stage
enriches it until the final PDF is produced.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Activity Level
# ---------------------------------------------------------------------------

@dataclass
class ActivitySpec:
    """A single student activity within a worksheet panel."""

    activity_type: str          # "trace", "circle_sound", "match", "word_search", etc.
    instructions: str           # Student-facing instruction text
    content: dict = field(default_factory=dict)
    # content is activity-specific, e.g.:
    #   trace:        {"words": ["cat", "hat", "bat"]}
    #   circle_sound: {"target_sound": "a", "words": ["cat", "dog", "map"]}
    #   match:        {"pairs": [["c", "at"], ["h", "at"]]}
    #   word_search:  {"grid_size": 8, "hidden_words": ["cat", "hat"]}


# ---------------------------------------------------------------------------
# Sheet Level
# ---------------------------------------------------------------------------

PANEL_COUNTS = {1: 3, 2: 3, 3: 2, 4: 1}   # sheet_number → panel_count
DIFFICULTY_MAP = {1: "intro", 2: "intro", 3: "level_up", 4: "summary"}


@dataclass
class SheetSpec:
    """One of the 4 worksheets in a lesson bundle."""

    sheet_number: int                           # 1-4
    panel_count: int = 0                        # auto-set from PANEL_COUNTS
    difficulty: str = ""                        # auto-set from DIFFICULTY_MAP
    activities: list[ActivitySpec] = field(default_factory=list)

    # Theme / narrative
    story_beat: str = ""                        # "The pirates board the ship"
    frame_prompt: str = ""                      # Full generate_image prompt

    # Populated during rendering
    rendered_panel_path: Optional[str] = None   # Path to raw worksheet PNG
    overlay_path: Optional[str] = None          # Path to framed worksheet PNG
    frame_art_paths: dict = field(default_factory=dict)
    # e.g. {"character_scene": "path.png", "bottom_frame": "...", ...}

    def __post_init__(self):
        if self.panel_count == 0:
            self.panel_count = PANEL_COUNTS.get(self.sheet_number, 3)
        if not self.difficulty:
            self.difficulty = DIFFICULTY_MAP.get(self.sheet_number, "intro")


# ---------------------------------------------------------------------------
# Theme Level
# ---------------------------------------------------------------------------

@dataclass
class ThemeSpec:
    """Defines the visual theme and narrative arc for the bundle."""

    name: str                                   # "pirate", "space", "castle"
    style_tokens: str = ""                      # "Kawaii vector art, thick outlines..."
    banner_prompt: str = ""                     # Prompt for title banner frame
    mascots: list[str] = field(default_factory=list)  # ["strawberry", "corn"]
    story_sequence: list[dict] = field(default_factory=list)
    # Each dict: {"phase": "01_voyage", "description": "...", "frame_prompt": "..."}


# ---------------------------------------------------------------------------
# Bundle Level (top-level spec)
# ---------------------------------------------------------------------------

@dataclass
class BundleSpec:
    """
    The complete blueprint for a 4-worksheet lesson bundle.

    Created by the Orchestrator, enriched by each agent:
      1. CurriculumArchitect → populates sheets + activities
      2. QualityAgent        → populates qa_verdict
      3. ImageGenerator      → populates frame_art_paths on each SheetSpec
      4. ModularFactory      → populates rendered_panel_path on each SheetSpec
      5. OverlayGenerator    → populates overlay_path on each SheetSpec
      6. CriticAgent         → populates critic_verdict
      7. BindBook            → populates pdf_path
    """

    # User inputs
    subject: str                                # "phonics", "math"
    topic: str                                  # "at_family", "addition_to_10"
    theme: ThemeSpec = field(default_factory=ThemeSpec)

    # Built by CurriculumArchitect
    sheets: list[SheetSpec] = field(default_factory=list)

    # QA results
    qa_verdict: Optional[dict] = None           # From QualityStandardsAgent
    critic_verdict: Optional[dict] = None       # From CriticAgent

    # Final output
    pdf_path: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """Quick check: do we have exactly 4 sheets with correct panel counts?"""
        if len(self.sheets) != 4:
            return False
        expected = [3, 3, 2, 1]
        return all(
            s.panel_count == e
            for s, e in zip(self.sheets, expected)
        )

    def summary(self) -> str:
        """Human-readable summary of the bundle spec."""
        lines = [
            f"Bundle: {self.subject} / {self.topic} — Theme: {self.theme.name}",
            f"Sheets: {len(self.sheets)}",
        ]
        for s in self.sheets:
            acts = ", ".join(a.activity_type for a in s.activities)
            lines.append(
                f"  Sheet {s.sheet_number}: {s.panel_count} panels "
                f"({s.difficulty}) — [{acts}]"
            )
        return "\n".join(lines)
