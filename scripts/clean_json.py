import json
import os

path = "project_state.json"
if os.path.exists(path):
    print(f"Cleaning {path}...")
    try:
        with open(path, "r") as f:
            data = json.load(f)
        
        # Write back to deduplicate keys
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print("JSON cleaned successfully.")
    except Exception as e:
        print(f"Error cleaning JSON: {e}")
else:
    print("project_state.json not found.")
