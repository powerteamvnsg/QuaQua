import json
import os

def create_project_state():
    """
    Creates project_state.json containing the syllabus.
    """
    LESSON_PLANS = [
        {"id": "Q01", "target": "-at", "words": ["bat", "cat", "rat"], "name": "Angry Ants Quest"},
        {"id": "Q02", "target": "-an", "words": ["fan", "pan", "man"], "name": "Angry Leprechaun Quest"},
        {"id": "Q03", "target": "-ap", "words": ["map", "cap", "tap"], "name": "Angry Snowman Quest"},
        {"id": "Q04", "target": "-ag", "words": ["bag", "tag", "wag"], "name": "Cloudy Day Quest"},
        {"id": "Q05", "target": "-am", "words": ["jam", "ham", "ram"], "name": "Escape Quest"},
        {"id": "Q06", "target": "-ad", "words": ["dad", "sad", "mad"], "name": "Fishy Business Quest"},
        {"id": "Q07", "target": "-et", "words": ["jet", "net", "wet"], "name": "Garden Gate Quest"},
        {"id": "Q08", "target": "-en", "words": ["hen", "pen", "ten"], "name": "Holey Moley Quest"},
        {"id": "Q09", "target": "-ed", "words": ["bed", "red", "fed"], "name": "Icy Mountain Quest"},
        {"id": "Q10", "target": "-it", "words": ["hit", "sit", "kit"], "name": "Lily Pond Quest"},
        {"id": "Q11", "target": "-in", "words": ["bin", "fin", "pin"], "name": "Lost Diamond Ring"},
        {"id": "Q12", "target": "-ig", "words": ["pig", "wig", "dig"], "name": "Pot of Gold Quest"},
        {"id": "Q13", "target": "-ip", "words": ["lip", "zip", "tip"], "name": "Racing Rabbit Quest"},
        {"id": "Q14", "target": "-ot", "words": ["hot", "pot", "dot"], "name": "Rainbow Bridge Quest"},
        {"id": "Q15", "target": "-og", "words": ["dog", "log", "fog"], "name": "Rainy Day Quest"},
        {"id": "Q16", "target": "-op", "words": ["mop", "hop", "top"], "name": "Sour Cherry Quest"},
        {"id": "Q17", "target": "-ox", "words": ["box", "fox", "ox"], "name": "Sunflower Quest"},
        {"id": "Q18", "target": "-ug", "words": ["bug", "rug", "mug"], "name": "Sunny Day Quest"},
        {"id": "Q19", "target": "-un", "words": ["sun", "bun", "run"], "name": "Turtle's Pace Quest"},
        {"id": "Q20", "target": "-ut", "words": ["nut", "cut", "hut"], "name": "Volcano Quest"},
        {"id": "Q21", "target": "-ub", "words": ["tub", "cub", "rub"], "name": "Lost Nut Quest"},
        {"id": "Q22", "target": "-ob", "words": ["cob", "sob", "rob"], "name": "Wet Grass Quest"},
        {"id": "Q23", "target": "-id", "words": ["kid", "lid", "hid"], "name": "Windy Day Quest"},
        {"id": "Q24", "target": "-ab", "words": ["cab", "lab", "tab"], "name": "Stone Medal Quest"},
        {"id": "Q25", "target": "-eg", "words": ["leg", "peg", "keg"], "name": "Iron Medal Quest"},
        {"id": "Q26", "target": "-ib", "words": ["bib", "rib", "nib"], "name": "Bronze Medal Quest"},
        {"id": "Q27", "target": "-ix", "words": ["six", "mix", "fix"], "name": "Silver Medal Quest"},
        {"id": "Q28", "target": "-od", "words": ["rod", "pod", "cod"], "name": "Gold Medal Quest"},
        {"id": "Q29", "target": "-um", "words": ["gum", "sum", "hum"], "name": "Diamond Medal Quest"}
    ]

    output_path = "project_state.json"
    with open(output_path, "w") as f:
        json.dump(LESSON_PLANS, f, indent=4)
    
    print(f"Stats: Generated {len(LESSON_PLANS)} lesson plans in {output_path}")

if __name__ == "__main__":
    create_project_state()