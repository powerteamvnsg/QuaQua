import json

from src.utils.path_utils import resolve

CONFIG_PATH = str(resolve('data/assets/characters/config.json'))

def get_character_squad(page_idx, count=3, full_object=False):
    """
    Returns a list of character names (or full objects) using round-robin rotation.
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            roster = config.get('characters', [])
    except:
        # Fallback roster if config is missing
        roster = [{"id": f"{i+1:02d}", "name": f"Character {i+1}", "role": "Friend", "action": "Helping"} for i in range(30)]
    
    if not roster:
        return [{"name": "Sir Strawberry"}] * count if full_object else ["Sir Strawberry"] * count

    squad = []
    r_len = len(roster)
    start_pos = (page_idx * count) % r_len
    
    for i in range(count):
        char = roster[(start_pos + i) % r_len]
        if full_object:
            squad.append(char)
        else:
            squad.append(char['name'])
    
    return squad
