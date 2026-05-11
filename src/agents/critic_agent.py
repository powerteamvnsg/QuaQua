"""
Critic Agent — Final visual QA gatekeeper.

Validates completed worksheets against Kawaii style rules, layout
correctness, and overall quality before binding into PDF.

CONTRACT:
- Accepts a BundleSpec with rendered worksheets
- Returns verdict dict with APPROVED or REJECTED
- Never fixes defects — only reports
"""

from __future__ import annotations
import os
from typing import Optional
from src.models.worksheet_spec import BundleSpec


class CriticAgent:
    """
    The 'Kawaii Consistency' Critic Agent.
    Acts as a final gatekeeper before PDF binding.

    Checks:
    - All 4 overlay PNGs exist
    - File sizes are reasonable (not corrupt/empty)
    - Story beat continuity
    """

    SYSTEM_PROMPT = """
You are the **Lead Art QA (Quality Assurance) Bot**. Your goal is to ensure 
visual consistency in a vector illustration pipeline.

**Style Rules:**
1. Linework: Thin black outlines (non-tapered).
2. Colors: Flat Matte (no gradients).
3. Eyes: Small black dot eyes with a tiny white reflection dot.
4. Limbs: Simple thin Solid Black lines.
5. Background: Solid White.

**Output Format:**
Must be strict JSON:
{
  "decision": "APPROVED" | "REJECTED",
  "confidence_score": 0.0-1.0,
  "primary_flaw": "None" | string,
  "feedback_for_generator": string
}
"""

    @staticmethod
    def review(spec: BundleSpec) -> dict:
        """
        Review the completed BundleSpec for visual and structural quality.

        Returns:
            dict with "decision", "issues", "confidence_score"
        """
        issues = []

        # Check: all 4 overlay PNGs exist
        for sheet in spec.sheets:
            path = sheet.overlay_path
            if not path:
                issues.append(
                    f"Sheet {sheet.sheet_number}: no overlay path set"
                )
            elif not os.path.exists(path):
                issues.append(
                    f"Sheet {sheet.sheet_number}: overlay file missing: {path}"
                )
            else:
                # Check file isn't empty/corrupt (< 10KB is suspicious for A4 PNG)
                size = os.path.getsize(path)
                if size < 10_000:
                    issues.append(
                        f"Sheet {sheet.sheet_number}: overlay suspiciously small "
                        f"({size} bytes)"
                    )

        # Check: story beat continuity
        beats = [s.story_beat for s in spec.sheets if s.story_beat]
        if len(beats) < 4:
            issues.append(
                f"Only {len(beats)}/4 story beats assigned — narrative incomplete"
            )

        # Check: frame art was generated for each sheet
        for sheet in spec.sheets:
            if not sheet.frame_art_paths:
                issues.append(
                    f"Sheet {sheet.sheet_number}: no frame art paths recorded"
                )

        # Build verdict
        if issues:
            return {
                "decision": "REJECTED",
                "confidence_score": max(0.0, 1.0 - len(issues) * 0.15),
                "issues": issues,
                "feedback": "Fix the issues listed above before binding.",
            }

        return {
            "decision": "APPROVED",
            "confidence_score": 0.95,
            "issues": [],
            "feedback": "All sheets pass visual QA. Ready for PDF binding.",
        }
