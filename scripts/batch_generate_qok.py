"""
QoK Level 1 - Batch Lesson Plan & Worksheet Generator
======================================================
Generates 25 Quests × 3 Competency Levels = 75 Worksheets

Competency Levels:
- Level 1: Introduction (recognition, simple matching)
- Level 2: Practice (application, multiple choice)
- Level 3: Mastery (challenge, independent work)

Output Structure:
QoK_Level1/
├── Quest_01_The_Garden_Gate/
│   ├── lesson_plan.json
│   ├── worksheet_level1.json
│   ├── worksheet_level2.json
│   ├── worksheet_level3.json
│   └── required_icons.json
├── Quest_02_The_Sunflower_Path/
│   └── ...
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# === CONFIGURATION ===

OUTPUT_BASE = Path(r"D:\moetvnpapers\k2-worksheet-generator\output\QoK_Level1")

# Quest definitions with themes and skills
QUESTS = [
    {"id": 1, "name": "The Garden Gate", "theme": "garden", "skill": "letter_recognition", "letters": ["A", "B", "C"]},
    {"id": 2, "name": "The Sunflower Path", "theme": "flowers", "skill": "initial_sounds", "focus": ["s", "f", "p"]},
    {"id": 3, "name": "The Walnut Tree", "theme": "trees", "skill": "rhyming", "word_family": "-at"},
    {"id": 4, "name": "The Rainy Day", "theme": "weather", "skill": "rhyming", "word_family": "-ain"},
    {"id": 5, "name": "Lost Nut Quest", "theme": "forest", "skill": "rhyming", "word_family": "-ut"},
    {"id": 6, "name": "Sunny Day Quest", "theme": "sunshine", "skill": "rhyming", "word_family": "-un"},
    {"id": 7, "name": "Cloudy Day Quest", "theme": "clouds", "skill": "rhyming", "word_family": "-oud"},
    {"id": 8, "name": "Sour Cherry Quest", "theme": "fruits", "skill": "final_phoneme", "word_family": "-at"},
    {"id": 9, "name": "Windy Day Quest", "theme": "wind", "skill": "rhyming", "word_family": "-ind"},
    {"id": 10, "name": "Holy Moly Quest", "theme": "garden", "skill": "rhyming", "word_family": "-ole"},
    {"id": 11, "name": "Lost Diamond Ring Quest", "theme": "treasure", "skill": "rhyming", "word_family": "-ing"},
    {"id": 12, "name": "Angry Ant Quest", "theme": "insects", "skill": "rhyming", "word_family": "-ant"},
    {"id": 13, "name": "Fishy Business Quest", "theme": "ocean", "skill": "rhyming", "word_family": "-ish"},
    {"id": 14, "name": "Lily Pond Quest", "theme": "pond", "skill": "rhyming", "word_family": "-ily"},
    {"id": 15, "name": "Icy Mountain Quest", "theme": "winter", "skill": "rhyming", "word_family": "-ice"},
    {"id": 16, "name": "Escape Quest", "theme": "adventure", "skill": "rhyming", "word_family": "-ape"},
    {"id": 17, "name": "Angry Snowman Quest", "theme": "snow", "skill": "rhyming", "word_family": "-ow"},
    {"id": 18, "name": "Final Destination", "theme": "journey", "skill": "rhyming", "word_family": "-est"},
    {"id": 19, "name": "Rainbow Bridge Quest", "theme": "rainbow", "skill": "rhyming", "word_family": "-ow"},
    {"id": 20, "name": "Stone Quest", "theme": "rocks", "skill": "rhyming", "word_family": "-one"},
    {"id": 21, "name": "Iron Quest", "theme": "metals", "skill": "rhyming", "word_family": "-on"},
    {"id": 22, "name": "Bronze Quest", "theme": "ancient", "skill": "rhyming", "word_family": "-onze"},
    {"id": 23, "name": "Silver Quest", "theme": "precious", "skill": "rhyming", "word_family": "-er"},
    {"id": 24, "name": "Gold Quest", "theme": "treasure", "skill": "rhyming", "word_family": "-old"},
    {"id": 25, "name": "Diamond Quest", "theme": "gems", "skill": "rhyming", "word_family": "-ond"},
]

# Word families for rhyming exercises
WORD_FAMILIES = {
    "-at": {"words": ["cat", "bat", "hat", "mat", "rat", "sat", "pat", "fat"], "icons": ["cat", "bat", "hat", "rat"]},
    "-un": {"words": ["sun", "run", "fun", "bun", "gun", "nun", "pun"], "icons": ["sun", "run"]},
    "-og": {"words": ["dog", "log", "fog", "hog", "jog", "frog"], "icons": ["dog", "log", "frog"]},
    "-ug": {"words": ["bug", "mug", "rug", "hug", "jug", "tug", "dug"], "icons": ["bug", "mug", "jug"]},
    "-ig": {"words": ["pig", "wig", "dig", "big", "fig", "jig"], "icons": ["pig", "wig"]},
    "-an": {"words": ["can", "fan", "man", "pan", "ran", "tan", "van"], "icons": ["can", "fan", "pan"]},
    "-en": {"words": ["pen", "hen", "ten", "men", "den", "yen"], "icons": ["pen", "hen"]},
    "-in": {"words": ["pin", "fin", "win", "bin", "tin", "sin"], "icons": ["pin", "fin"]},
    "-ot": {"words": ["pot", "hot", "got", "dot", "lot", "not", "cot"], "icons": ["pot"]},
    "-ed": {"words": ["bed", "red", "led", "fed", "wed", "sled"], "icons": ["bed"]},
    "-et": {"words": ["net", "pet", "wet", "bet", "jet", "set", "vet"], "icons": ["net"]},
    "-ut": {"words": ["nut", "cut", "but", "hut", "gut", "shut"], "icons": ["nut"]},
    "-ain": {"words": ["rain", "train", "brain", "chain", "drain", "grain"], "icons": ["rain"]},
    "-ind": {"words": ["wind", "find", "kind", "mind", "bind"], "icons": ["wind"]},
    "-ole": {"words": ["hole", "mole", "pole", "sole", "role"], "icons": ["mole"]},
    "-ing": {"words": ["ring", "king", "sing", "wing", "sting"], "icons": ["ring", "king"]},
    "-ant": {"words": ["ant", "plant", "slant", "chant"], "icons": ["ant"]},
    "-ish": {"words": ["fish", "dish", "wish", "swish"], "icons": ["fish"]},
    "-ily": {"words": ["lily", "silly", "hilly", "frilly"], "icons": ["lily"]},
    "-ice": {"words": ["ice", "mice", "dice", "rice", "nice", "slice"], "icons": ["ice", "mice"]},
    "-ape": {"words": ["cape", "tape", "grape", "escape"], "icons": ["cape"]},
    "-ow": {"words": ["snow", "bow", "row", "flow", "glow"], "icons": ["snow", "bow"]},
    "-est": {"words": ["nest", "best", "rest", "test", "vest", "west"], "icons": ["nest"]},
    "-one": {"words": ["stone", "bone", "cone", "phone", "zone"], "icons": ["stone", "bone"]},
    "-on": {"words": ["iron", "lion", "upon"], "icons": ["iron", "lion"]},
    "-onze": {"words": ["bronze"], "icons": ["bronze"]},
    "-er": {"words": ["silver", "river", "flower", "power"], "icons": ["silver", "flower"]},
    "-old": {"words": ["gold", "cold", "bold", "hold", "fold", "sold"], "icons": ["gold"]},
    "-ond": {"words": ["diamond", "pond", "bond", "fond"], "icons": ["diamond", "pond"]},
    "-oud": {"words": ["cloud", "loud", "proud"], "icons": ["cloud"]},
}

COMPETENCY_LEVELS = {
    1: {
        "name": "Introduction",
        "description": "Recognition and simple matching",
        "task_types": ["match_picture_to_word", "circle_rhyming_pair"],
        "num_questions": 3,
        "distractors": 2
    },
    2: {
        "name": "Practice", 
        "description": "Application and multiple choice",
        "task_types": ["multiple_choice_rhyme", "find_odd_one_out"],
        "num_questions": 4,
        "distractors": 3
    },
    3: {
        "name": "Mastery",
        "description": "Challenge and independent work",
        "task_types": ["complete_the_rhyme", "sort_by_word_family"],
        "num_questions": 5,
        "distractors": 4
    }
}


def generate_lesson_plan(quest: Dict) -> Dict:
    """Generate a lesson plan for a quest."""
    word_family = quest.get("word_family", "-at")
    family_data = WORD_FAMILIES.get(word_family, WORD_FAMILIES["-at"])
    
    return {
        "quest_id": f"QOK-L1-Q{quest['id']:02d}",
        "quest_name": quest["name"],
        "theme": quest["theme"],
        "skill_type": quest["skill"],
        "word_family": word_family,
        "learning_objectives": [
            f"Identify words that rhyme with the {word_family} word family",
            f"Match pictures to rhyming words",
            f"Distinguish rhyming from non-rhyming words"
        ],
        "target_words": family_data["words"][:6],
        "required_icons": family_data["icons"],
        "worksheets": [
            {"level": 1, "name": "Introduction", "file": "worksheet_level1.json"},
            {"level": 2, "name": "Practice", "file": "worksheet_level2.json"},
            {"level": 3, "name": "Mastery", "file": "worksheet_level3.json"},
        ],
        "generated_at": datetime.now().isoformat()
    }


def generate_worksheet(quest: Dict, level: int) -> Dict:
    """Generate a worksheet for a specific competency level."""
    word_family = quest.get("word_family", "-at")
    family_data = WORD_FAMILIES.get(word_family, WORD_FAMILIES["-at"])
    level_config = COMPETENCY_LEVELS[level]
    
    words = family_data["words"]
    icons = family_data["icons"]
    
    questions = []
    for i in range(level_config["num_questions"]):
        if words:
            target_word = words[i % len(words)]
            questions.append({
                "question_id": i + 1,
                "type": level_config["task_types"][0],
                "target_word": target_word,
                "target_icon": icons[i % len(icons)] if icons else target_word,
                "options": words[:level_config["distractors"] + 1],
                "correct_answer": target_word
            })
    
    return {
        "worksheet_id": f"QOK-L1-Q{quest['id']:02d}-W{level}",
        "quest_name": quest["name"],
        "competency_level": level,
        "level_name": level_config["name"],
        "description": level_config["description"],
        "word_family": word_family,
        "questions": questions,
        "required_icons": icons,
        "generated_at": datetime.now().isoformat()
    }


def compile_required_icons(quest: Dict, lesson_plan: Dict, worksheets: List[Dict]) -> Dict:
    """Compile all required icons for a quest."""
    all_icons = set()
    
    # From lesson plan
    all_icons.update(lesson_plan.get("required_icons", []))
    
    # From worksheets
    for ws in worksheets:
        all_icons.update(ws.get("required_icons", []))
        for q in ws.get("questions", []):
            if q.get("target_icon"):
                all_icons.add(q["target_icon"])
    
    return {
        "quest_id": f"QOK-L1-Q{quest['id']:02d}",
        "quest_name": quest["name"],
        "icons": sorted(list(all_icons)),
        "count": len(all_icons),
        "generated_at": datetime.now().isoformat()
    }


def generate_all():
    """Generate all 25 quests with 3 worksheets each."""
    all_icons = set()
    summary = {
        "total_quests": 25,
        "worksheets_per_quest": 3,
        "total_worksheets": 75,
        "quests": []
    }
    
    for quest in QUESTS:
        quest_folder = OUTPUT_BASE / f"Quest_{quest['id']:02d}_{quest['name'].replace(' ', '_')}"
        quest_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate lesson plan
        lesson_plan = generate_lesson_plan(quest)
        with open(quest_folder / "lesson_plan.json", "w") as f:
            json.dump(lesson_plan, f, indent=2)
        
        # Generate 3 worksheets
        worksheets = []
        for level in [1, 2, 3]:
            worksheet = generate_worksheet(quest, level)
            worksheets.append(worksheet)
            with open(quest_folder / f"worksheet_level{level}.json", "w") as f:
                json.dump(worksheet, f, indent=2)
        
        # Compile required icons
        icons = compile_required_icons(quest, lesson_plan, worksheets)
        with open(quest_folder / "required_icons.json", "w") as f:
            json.dump(icons, f, indent=2)
        
        all_icons.update(icons["icons"])
        
        summary["quests"].append({
            "id": quest["id"],
            "name": quest["name"],
            "folder": str(quest_folder),
            "icons_needed": icons["icons"]
        })
        
        print(f"✅ Quest {quest['id']:02d}: {quest['name']} - {len(icons['icons'])} icons needed")
    
    # Save master summary
    summary["all_unique_icons"] = sorted(list(all_icons))
    summary["total_unique_icons"] = len(all_icons)
    summary["generated_at"] = datetime.now().isoformat()
    
    with open(OUTPUT_BASE / "master_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"✅ GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total Quests: {summary['total_quests']}")
    print(f"Total Worksheets: {summary['total_worksheets']}")
    print(f"Total Unique Icons Needed: {summary['total_unique_icons']}")
    print(f"\nIcons: {', '.join(summary['all_unique_icons'])}")
    
    return summary


if __name__ == "__main__":
    generate_all()
