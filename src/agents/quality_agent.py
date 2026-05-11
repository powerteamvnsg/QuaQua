"""
Quality Standards Agent — Audits BundleSpec for commercial readiness.

Sole responsibility: Find defects. Never fixes them, never generates alternatives.

CONTRACT:
- Accepts BundleSpec
- Returns QAVerdict (PASS or FAIL)
- BLOCKS pipeline on P0/P1 defects
- NEVER fixes defects or generates alternatives
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from src.models.worksheet_spec import BundleSpec, PANEL_COUNTS


# ---------------------------------------------------------------------------
# QA data structures
# ---------------------------------------------------------------------------

@dataclass
class Defect:
    """A single QA defect."""
    defect_id: str
    message: str
    severity: str = "P0"   # P0 = hard blocker, P1 = release blocker, P2 = warning

    def __repr__(self):
        return f"[{self.severity}] {self.defect_id}: {self.message}"


@dataclass
class QAVerdict:
    """Final QA verdict."""
    status: str                                 # "PASS" or "FAIL"
    defects: list[Defect] = field(default_factory=list)
    release_blocked: bool = False

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "defects": [
                {"id": d.defect_id, "message": d.message, "severity": d.severity}
                for d in self.defects
            ],
            "release_blocked": self.release_blocked,
        }

    def __repr__(self):
        return f"QAVerdict({self.status}, {len(self.defects)} defects, blocked={self.release_blocked})"


# ---------------------------------------------------------------------------
# Banned content lists
# ---------------------------------------------------------------------------

BANNED_WORDS = [
    "explore", "practice", "get familiar with",
    "understand", "fun", "introduction to",
]

BANNED_INSTRUCTION_PHRASES = [
    "picture", "image", "photo", "drawing", "illustration",
]


# ---------------------------------------------------------------------------
# The Agent
# ---------------------------------------------------------------------------

class QualityStandardsAgent:
    """
    Audits a BundleSpec against strict commercial readiness rules.

    Checks:
    - Structural correctness (4 sheets, correct panel counts)
    - Word diversity (no repeated word sets across sheets)
    - Progressive difficulty (intro → level_up → summary)
    - Text-only policy (no image references in instructions)
    - Language hygiene (no banned filler words)
    """

    @staticmethod
    def verify(spec: BundleSpec) -> QAVerdict:
        """
        Run a comprehensive audit on the BundleSpec.

        Returns QAVerdict with PASS or FAIL status.
        FAIL verdict blocks the rendering pipeline.
        """
        defects: list[Defect] = []

        # ==================== P0 RULES (Hard Blockers) ====================

        # P0-001: Must have exactly 4 sheets
        if len(spec.sheets) != 4:
            defects.append(Defect(
                "P0-001",
                f"Expected 4 sheets, got {len(spec.sheets)}",
                "P0",
            ))

        # P0-002: Each sheet must have correct panel count
        for sheet in spec.sheets:
            expected = PANEL_COUNTS.get(sheet.sheet_number, 0)
            if sheet.panel_count != expected:
                defects.append(Defect(
                    "P0-002",
                    f"Sheet {sheet.sheet_number}: expected {expected} panels, "
                    f"got {sheet.panel_count}",
                    "P0",
                ))

        # P0-003: No empty activity lists
        for sheet in spec.sheets:
            if len(sheet.activities) == 0:
                defects.append(Defect(
                    "P0-003",
                    f"Sheet {sheet.sheet_number}: no activities defined",
                    "P0",
                ))

        # P0-004: Activity count must match panel count
        for sheet in spec.sheets:
            if len(sheet.activities) != sheet.panel_count:
                defects.append(Defect(
                    "P0-004",
                    f"Sheet {sheet.sheet_number}: {len(sheet.activities)} activities "
                    f"but {sheet.panel_count} panels",
                    "P0",
                ))

        # P0-005: Text-only policy — no image references in instructions
        for sheet in spec.sheets:
            for act in sheet.activities:
                for phrase in BANNED_INSTRUCTION_PHRASES:
                    if phrase.lower() in act.instructions.lower():
                        defects.append(Defect(
                            "P0-005",
                            f"Sheet {sheet.sheet_number}, '{act.activity_type}': "
                            f"instructions contain banned phrase '{phrase}'",
                            "P0",
                        ))

        # ==================== P1 RULES (Release Blockers) ====================

        # P1-001: Word diversity — no identical word sets between sheets 1 and 2
        if len(spec.sheets) >= 2:
            words_1 = _extract_words(spec.sheets[0])
            words_2 = _extract_words(spec.sheets[1])
            if words_1 and words_2 and words_1 == words_2:
                defects.append(Defect(
                    "P1-001",
                    "Sheets 1 and 2 have identical word sets — no diversity",
                    "P1",
                ))

        # P1-002: Progressive difficulty — sheets must have correct difficulty labels
        expected_diff = ["intro", "intro", "level_up", "summary"]
        for i, sheet in enumerate(spec.sheets):
            if i < len(expected_diff) and sheet.difficulty != expected_diff[i]:
                defects.append(Defect(
                    "P1-002",
                    f"Sheet {sheet.sheet_number}: expected difficulty "
                    f"'{expected_diff[i]}', got '{sheet.difficulty}'",
                    "P1",
                ))

        # P1-003: Theme must have 4 story beats
        if len(spec.theme.story_sequence) < 4:
            defects.append(Defect(
                "P1-003",
                f"Theme '{spec.theme.name}' has only "
                f"{len(spec.theme.story_sequence)} story beats (need 4)",
                "P1",
            ))

        # P1-004: Each sheet should have a story beat assigned
        for sheet in spec.sheets:
            if not sheet.story_beat:
                defects.append(Defect(
                    "P1-004",
                    f"Sheet {sheet.sheet_number}: no story beat assigned",
                    "P1",
                ))

        # ==================== P2 RULES (Warnings) ====================

        # P2-001: Language hygiene — banned filler words in instructions
        all_text = " ".join(
            act.instructions
            for sheet in spec.sheets
            for act in sheet.activities
        )
        for bad in BANNED_WORDS:
            if bad.lower() in all_text.lower():
                defects.append(Defect(
                    "P2-001",
                    f"Found banned filler word '{bad}' in instructions",
                    "P2",
                ))

        # P2-002: Duplicate words within same activity
        for sheet in spec.sheets:
            for act in sheet.activities:
                words = act.content.get("words", [])
                if len(words) != len(set(w.lower() for w in words)):
                    defects.append(Defect(
                        "P2-002",
                        f"Sheet {sheet.sheet_number}, '{act.activity_type}': "
                        f"duplicate words in content",
                        "P2",
                    ))

        # ==================== VERDICT ====================

        p0 = [d for d in defects if d.severity == "P0"]
        p1 = [d for d in defects if d.severity == "P1"]

        if p0 or p1:
            return QAVerdict(status="FAIL", defects=defects, release_blocked=True)

        p2 = [d for d in defects if d.severity == "P2"]
        if p2:
            return QAVerdict(status="PASS", defects=p2, release_blocked=False)

        return QAVerdict(status="PASS", defects=[], release_blocked=False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_words(sheet) -> set:
    """Pull all words from a sheet's activities for comparison."""
    words = set()
    for act in sheet.activities:
        for w in act.content.get("words", []):
            words.add(w.lower() if isinstance(w, str) else str(w))
    return words
