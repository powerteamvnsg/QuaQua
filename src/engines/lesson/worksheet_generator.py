"""
Worksheet Generator Agent — Converts BundleSpec activities into renderable content.

Sole responsibility: Mechanical conversion from curriculum specs to panel-ready
data for modular_factory.py.  Never invents new content.

CONTRACT:
- Accepts BundleSpec with activities already assigned by CurriculumArchitect
- Enriches each ActivitySpec.content with render-ready fields
- Never modifies the activity types or words chosen by the architect
"""

from __future__ import annotations
from src.models.worksheet_spec import BundleSpec, SheetSpec, ActivitySpec


# ---------------------------------------------------------------------------
# Instruction Templates (Text-Only Policy)
# ---------------------------------------------------------------------------

BANNED_INSTRUCTION_PHRASES = ["picture", "image", "photo", "drawing", "illustration"]


# ---------------------------------------------------------------------------
# The Generator
# ---------------------------------------------------------------------------

class WorksheetGenerator:
    """
    Enriches BundleSpec activities with render-ready content.

    For each activity, adds layout hints and task data that
    modular_factory.py can directly consume to draw panels.
    """

    @staticmethod
    def generate(spec: BundleSpec) -> BundleSpec:
        """
        Process all sheets in the BundleSpec, enriching activity content
        with render-ready fields.

        Returns the same BundleSpec (mutated in place) with enriched content.
        """
        for sheet in spec.sheets:
            for activity in sheet.activities:
                WorksheetGenerator._enrich_activity(activity, sheet)

        return spec

    @staticmethod
    def _enrich_activity(activity: ActivitySpec, sheet: SheetSpec) -> None:
        """Add render-ready fields to an activity's content dict."""

        content = activity.content
        act_type = activity.activity_type

        # Add common render hints
        content["_render"] = {
            "sheet_number": sheet.sheet_number,
            "panel_count": sheet.panel_count,
            "difficulty": sheet.difficulty,
        }

        # Type-specific enrichment
        if act_type == "trace":
            # Add dotted-line rendering hints
            words = content.get("words", [])
            content["_render"]["items"] = [
                {"word": w, "style": "dotted", "font_size": 48}
                for w in words
            ]

        elif act_type == "circle_sound":
            words = content.get("words", [])
            target = content.get("target_sound", "")
            content["_render"]["items"] = [
                {"word": w, "highlight": target in w.lower()}
                for w in words
            ]

        elif act_type == "match":
            pairs = content.get("pairs", [])
            content["_render"]["left_column"] = [p[0] for p in pairs if len(p) >= 2]
            content["_render"]["right_column"] = [p[1] for p in pairs if len(p) >= 2]

        elif act_type == "multiple_choice":
            words = content.get("words", [])
            n_opts = content.get("options_per_word", 3)
            content["_render"]["items"] = [
                {"prompt": w, "num_options": n_opts}
                for w in words
            ]

        elif act_type == "fill_blank":
            words = content.get("words", [])
            pos = content.get("blank_position", "first")
            content["_render"]["items"] = [
                {"word": w, "blank_index": 0 if pos == "first" else -1}
                for w in words
            ]

        elif act_type == "word_search":
            content["_render"]["grid_size"] = content.get("grid_size", 8)
            content["_render"]["word_list"] = content.get("hidden_words", [])

        elif act_type == "unscramble":
            import random
            words = content.get("words", [])
            content["_render"]["items"] = []
            for w in words:
                letters = list(w)
                random.shuffle(letters)
                content["_render"]["items"].append({
                    "scrambled": "".join(letters),
                    "answer": w,
                    "num_blanks": len(w),
                })

        elif act_type == "crossword":
            words = content.get("words", [])
            clues = content.get("clues", [])
            content["_render"]["entries"] = [
                {"word": w, "clue": clues[i] if i < len(clues) else f"Clue {i+1}"}
                for i, w in enumerate(words)
            ]

        elif act_type == "maze":
            content["_render"]["correct_words"] = content.get("collecting_words", [])
            content["_render"]["distractor_words"] = content.get("incorrect_words", [])

        elif act_type in ("story_finish", "creative_write"):
            content["_render"]["lined_area"] = True
            content["_render"]["num_lines"] = 5 if sheet.difficulty == "summary" else 3

        # Validate: no banned phrases snuck in
        instr = activity.instructions
        for phrase in BANNED_INSTRUCTION_PHRASES:
            if phrase.lower() in instr.lower():
                raise ValueError(
                    f"Activity '{act_type}' contains banned phrase '{phrase}' "
                    f"(TEXT-ONLY policy violation)"
                )
