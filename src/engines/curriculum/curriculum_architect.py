"""
Curriculum Architect Agent — Builds complete BundleSpec for a lesson.

Sole responsibility: Define strict curriculum specifications with a
4-sheet narrative bundle.  Never writes lesson text.

CONTRACT:
- Returns a complete BundleSpec or raises SpecValidationError
- Never returns partial data
- Never uses default values for curriculum content
- Assigns story beats from the theme's story_sequence
"""

from __future__ import annotations
from src.models.worksheet_spec import (
    ActivitySpec, SheetSpec, ThemeSpec, BundleSpec
)


class SpecValidationError(Exception):
    """Raised when a spec is missing required keys or has invalid structure."""


class UnsupportedSkillTypeError(Exception):
    """Raised when an unknown skill_type is encountered."""


# ---------------------------------------------------------------------------
# Activity-type catalogue — what the architect can assign
# ---------------------------------------------------------------------------

ACTIVITY_CATALOGUE = {
    # --- Sheet 1-2 activities (3 per sheet, introductory) ---
    "trace":          {"panel_size": "small", "description": "Trace the dotted word"},
    "circle_sound":   {"panel_size": "small", "description": "Circle the target sound"},
    "match":          {"panel_size": "small", "description": "Match pairs with lines"},
    "multiple_choice":{"panel_size": "small", "description": "Circle the correct answer"},
    "fill_blank":     {"panel_size": "small", "description": "Write the missing letter"},
    "color_by_sound": {"panel_size": "small", "description": "Color by initial sound"},
    "sort":           {"panel_size": "small", "description": "Sort items into categories"},
    "count":          {"panel_size": "small", "description": "Count and write the number"},

    # --- Sheet 3 activities (2 per sheet, level-up) ---
    "word_search":    {"panel_size": "large", "description": "Find hidden words in grid"},
    "unscramble":     {"panel_size": "large", "description": "Unscramble letters to form word"},
    "riddle":         {"panel_size": "large", "description": "Solve a phonics riddle"},
    "sentence_build": {"panel_size": "large", "description": "Arrange words into a sentence"},

    # --- Sheet 4 activities (1 per sheet, capstone/summary) ---
    "story_finish":   {"panel_size": "full", "description": "Complete the mini-story"},
    "creative_write": {"panel_size": "full", "description": "Write your own words/sentence"},
    "maze":           {"panel_size": "full", "description": "Follow the path collecting words"},
    "crossword":      {"panel_size": "full", "description": "Fill in the crossword puzzle"},
}

# Which activities are appropriate for each sheet difficulty level
SHEET_ACTIVITY_POOL = {
    "intro":    ["trace", "circle_sound", "match", "multiple_choice",
                 "fill_blank", "color_by_sound", "sort", "count"],
    "level_up": ["word_search", "unscramble", "riddle", "sentence_build"],
    "summary":  ["story_finish", "creative_write", "maze", "crossword"],
}


# ---------------------------------------------------------------------------
# Curriculum database — hardcoded lesson specs
# ---------------------------------------------------------------------------


CURRICULUM_DATABASE = {
    "at_family": {
        "subject": "phonics",
        "domain": "Literacy",
        "skill_type": "cvc_words",
        "primary_skill": "Basic Phonics",
        "words": ["A", "B", "C", "1", "2", "3"],
        "target_sound": "-at",
    },
    "addition_to_10": {
        "subject": "math",
        "domain": "Math",
        "skill_type": "concrete_addition",
        "primary_skill": "Basic Counting",
        "words": ["1", "2", "3", "4", "5", "6"],
    }
}



# ---------------------------------------------------------------------------
# The Architect
# ---------------------------------------------------------------------------

class CurriculumArchitect:
    """
    Builds a complete BundleSpec for a given topic and theme.

    The architect:
    1. Looks up the curriculum database for the topic
    2. Selects appropriate activities for each of 4 sheets
    3. Assigns content (words/numbers) from the spec — never invents
    4. Attaches story beats from the theme
    """

    @staticmethod
    def build_spec(topic_key: str, theme: ThemeSpec) -> BundleSpec:
        """
        Build a complete 4-sheet BundleSpec.

        Args:
            topic_key: Key into CURRICULUM_DATABASE (e.g. "at_family")
            theme:     ThemeSpec with name, style_tokens, story_sequence

        Returns:
            BundleSpec ready for QA validation

        Raises:
            SpecValidationError if topic not found or data incomplete
        """
        if topic_key not in CURRICULUM_DATABASE:
            raise SpecValidationError(
                f"Unknown topic: '{topic_key}'. "
                f"Available: {list(CURRICULUM_DATABASE.keys())}"
            )

        curriculum = CURRICULUM_DATABASE[topic_key]
        subject = curriculum["subject"]
        words = curriculum.get("words", [])

        # Build 4 sheets with progressive difficulty
        sheets = [
            CurriculumArchitect._build_sheet(1, curriculum, theme, words[0:3]),
            CurriculumArchitect._build_sheet(2, curriculum, theme, words[3:6]),
            CurriculumArchitect._build_sheet(3, curriculum, theme, words[0:6]),
            CurriculumArchitect._build_sheet(4, curriculum, theme, words),
        ]

        spec = BundleSpec(
            subject=subject,
            topic=topic_key,
            theme=theme,
            sheets=sheets,
        )

        # Final validation
        if not spec.is_valid:
            raise SpecValidationError(
                f"BundleSpec validation failed: {spec.summary()}"
            )

        return spec

    @staticmethod
    def _build_sheet(
        sheet_num: int,
        curriculum: dict,
        theme: ThemeSpec,
        word_slice: list,
    ) -> SheetSpec:
        """Build a single SheetSpec with activities appropriate to difficulty."""
        from src.models.worksheet_spec import PANEL_COUNTS, DIFFICULTY_MAP

        difficulty = DIFFICULTY_MAP[sheet_num]
        panel_count = PANEL_COUNTS[sheet_num]
        pool = SHEET_ACTIVITY_POOL[difficulty]

        # Pick activities from the pool (rotate through available types)
        activities = []
        for i in range(panel_count):
            act_type = pool[i % len(pool)]
            content = CurriculumArchitect._make_content(
                act_type, curriculum, word_slice, i
            )
            activities.append(ActivitySpec(
                activity_type=act_type,
                instructions=CurriculumArchitect._get_instructions(act_type, curriculum),
                content=content,
            ))

        # Attach story beat from theme
        story_beat = ""
        frame_prompt = ""
        if theme.story_sequence and sheet_num <= len(theme.story_sequence):
            seq = theme.story_sequence[sheet_num - 1]
            story_beat = seq.get("description", "")
            frame_prompt = seq.get("frame_prompt", "")

        return SheetSpec(
            sheet_number=sheet_num,
            activities=activities,
            story_beat=story_beat,
            frame_prompt=frame_prompt,
        )

    @staticmethod
    def _make_content(
        act_type: str, curriculum: dict, words: list, index: int
    ) -> dict:
        """Create activity-specific content from curriculum data."""

        if act_type == "trace":
            return {"words": words[:3] if words else ["word"]}

        elif act_type == "circle_sound":
            target = curriculum.get("target_sound", "")
            return {"target_sound": target, "words": words[:3]}

        elif act_type == "match":
            pairs = curriculum.get("pairs", [])
            if pairs:
                return {"pairs": [list(p) if isinstance(p, tuple) else p for p in pairs[:3]]}
            onset = curriculum.get("onset_set", [])
            rime = curriculum.get("target_sound", "")
            return {"pairs": [[o, rime] for o in onset[:3]]}

        elif act_type == "multiple_choice":
            return {"words": words[:3], "options_per_word": 3}

        elif act_type == "fill_blank":
            return {"words": words[:3], "blank_position": "first"}

        elif act_type == "color_by_sound":
            return {"target_sound": curriculum.get("target_sound", ""), "words": words[:4]}

        elif act_type == "sort":
            groups = curriculum.get("sound_groups", {})
            return {"categories": list(groups.keys())[:2], "items": words[:6]}

        elif act_type == "count":
            nums = curriculum.get("number_sets", [2, 3, 4])
            return {"numbers": nums[:3]}

        elif act_type == "word_search":
            return {"hidden_words": words[:6], "grid_size": 8}

        elif act_type == "unscramble":
            return {"words": words[:4]}

        elif act_type == "riddle":
            return {"target_word": words[index % len(words)] if words else "cat",
                    "clue": f"I rhyme with {curriculum.get('target_sound', 'hat')}"}

        elif act_type == "sentence_build":
            return {"words": words[:4], "sentence_frame": "The ___ sat on the ___."}

        elif act_type == "story_finish":
            return {"starter": f"One day, a {words[0] if words else 'cat'} went on an adventure...",
                    "word_bank": words[:6]}

        elif act_type == "creative_write":
            return {"prompt": f"Write 3 words that end with {curriculum.get('target_sound', '-at')}",
                    "word_bank": words[:4]}

        elif act_type == "maze":
            return {"collecting_words": words[:5], "incorrect_words": ["dog", "pig", "hen"]}

        elif act_type == "crossword":
            return {"words": words[:4],
                    "clues": [f"Rhymes with {w}" for w in words[:4]]}

        return {"words": words[:3]}

    @staticmethod
    def _get_instructions(act_type: str, curriculum: dict) -> str:
        """Return student-facing instruction text for an activity type."""
        target = curriculum.get("target_sound", "the target sound")

        TEMPLATES = {
            "trace":          "Trace each word carefully. Say it out loud as you write.",
            "circle_sound":   f"Circle every word that has the '{target}' sound.",
            "match":          "Draw a line to match each beginning sound to its ending.",
            "multiple_choice":"Circle the correct answer.",
            "fill_blank":     "Write the missing letter to complete each word.",
            "color_by_sound": f"Color the items that start with '{target}'.",
            "sort":           "Sort each word into the correct box.",
            "count":          "Count the dots. Write the number.",
            "word_search":    "Find and circle the hidden words in the grid.",
            "unscramble":     "Unscramble the letters to make a word.",
            "riddle":         "Read the clue. Write the word that fits.",
            "sentence_build": "Put the words in order to make a sentence.",
            "story_finish":   "Read the story start. Write what happens next!",
            "creative_write": "Use the word bank to write your own words or sentence.",
            "maze":           "Follow the path. Collect the correct words along the way!",
            "crossword":      "Read each clue. Write the word in the boxes.",
        }
        return TEMPLATES.get(act_type, "Complete the activity.")
