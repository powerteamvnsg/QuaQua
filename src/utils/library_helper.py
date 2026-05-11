
import os
import shutil

LIBRARY_DIR = r"d:\AntiGravity Projects\k2-worksheet-generator\CharacterGen\Sprite Sheets\Library"

CATEGORIES = {
    "Characters": [
        "character", "boy", "girl", "man", "woman", "father", "son", "mother", "daughter",
        "human", "person", "astronaut", "wizard", "princess", "prince", "king", "queen",
        "superhero", "hero", "fireman", "firefighter", "doctor", "nurse", "police", "cop",
        "chef", "cook", "gardener", "plumber", "teacher", "student", "detective", "pilot",
        "racer", "mechanic", "artist", "writer", "musician", "dancer", "athlete", "player",
        "baby", "kid", "child", "friend", "running", "walking", "jumping", "sitting",
        "standing", "digging", "flying", "waving", "crying", "reading", "writing",
        "playing", "working", "holding_hands", "elf", "fairy", "gnome", "clown",
        "spinach_nurse", "onion_police", "carrot_farmer", "broccoli_bowtie", "garlic_gardener",
        "mango_wizard", "potato_plumber", "potato_detective", "potato_mechanic", "potato_scientist",
        "turnip_watching", "turnip_reading", "strawberry_gardener", "lemon_student", 
        "pineapple_graduate", "pineapple_teacher", "plum_pilot", "radish_racer",
        "asparagus_strong", "asparagus_musician", "mangosteen_musician", "grapes_meditating",
        "watermelon_gentleman", "watermelon_doctor", "corn_superhero", "apple_dancing",
        "apple_artist", "pear_cute", "avocado_cute" # Cute often implies character in this set
    ],
    "Food": [
        "apple", "banana", "pear", "grape", "lemon", "lime", "orange", "strawberry", "blueberry", 
        "raspberry", "cherry", "plum", "fig", "mango", "mangosteen", "pineapple", "watermelon", "melon",
        "corn", "carrot", "pea", "bean", "broccoli", "cauliflower", "asparagus", "spinach", 
        "lettuce", "cabbage", "onion", "garlic", "leek", "turnip", "radish", "beet", "potato", 
        "tomato", "cucumber", "eggplant", "pepper", "chili", "mushroom", "pumpkin", "squash",
        "pizza", "burger", "hamburger", "cheeseburger", "hotdog", "taco", "sandwich", "fries", 
        "popcorn", "chip", "cookie", "donut", "cake", "cupcake", "ice_cream", "chocolate", "candy", 
        "bread", "toast", "cereal", "pancake", "waffle", "egg", "milk", "cheese", "butter", 
        "soup", "ramen", "sushi", "jam", "honey", "tea", "coffee", "juice", "soda", "water", "drink",
        "meat", "ribs", "steak", "chicken_leg", "fish_raw", "fish_cooked", "shrimp_cooked",
        "muffin", "pretzel", "biscuit", "pie", "tart", "bagel", "croissant"
    ],
    "Animals": [
        "cat", "dog", "mouse", "rat", "rabbit", "bunny", "squirrel", "chipmunk", "hedgehog", 
        "bear", "fox", "wolf", "lion", "tiger", "elephant", "monkey", "giraffe", "zebra", 
        "horse", "cow", "pig", "sheep", "goat", "chicken", "rooster", "hen", "duck", "goose", 
        "bird", "owl", "eagle", "hawk", "parrot", "penguin", "frog", "toad", "turtle", 
        "snake", "lizard", "dinosaur", "dragon", "fish", "whale", "dolphin", "shark", 
        "octopus", "crab", "lobster", "shrimp", "starfish", "jellyfish", "snail", "slug", 
        "butterfly", "bee", "ladybug", "ant", "spider", "worm", "fly", "mosquito", "bug", "insect",
        "pet"
    ],
    "Transport": [
        "car", "bus", "truck", "van", "taxi", "cab", "ambulance", "police_car", "fire_truck", 
        "train", "subway", "metro", "tram", "plane", "airplane", "jet", "helicopter", "rocket", 
        "spaceship", "ufo", "boat", "ship", "yacht", "submarine", "bicycle", "bike", "scooter", 
        "motorcycle", "motorbike", "skateboard", "skate", "wagon", "tractor", "bulldozer", 
        "excavator", "crane", "drone", "vehicle"
    ],
    "Plants": [
        "flower", "rose", "tulip", "daisy", "sunflower", "orchid", "lily", "lotus", 
        "hibiscus", "lavender", "blossom", "bloom", "plant", "tree", "bush", "shrub", 
        "grass", "leaf", "leaves", "vine", "branch", "stem", "root", "cactus", "cacti", 
        "fern", "moss", "wreath", "floral", "garden", "nature", "log", "stump", "wood"
    ],
    "Furniture": [
        "table", "chair", "desk", "sofa", "couch", "bed", "crib", "dresser", "bureau", 
        "cabinet", "shelf", "shelves", "bookcase", "wardrobe", "closet", "lamp", "light", 
        "rug", "carpet", "mat", "curtain", "drape", "blind", "mirror", "clock", "bench", 
        "stool", "seat", "sink", "toilet", "bathtub", "shower", "stove", "oven", "fridge", 
        "refrigerator", "freezer", "microwave", "dishwasher", "washer", "dryer", "furniture",
        "nightstand", "armchair", "beanbag"
    ],
    "Clothes": [
        "shirt", "t-shirt", "top", "blouse", "pants", "trousers", "jeans", "shorts", 
        "skirt", "dress", "gown", "coat", "jacket", "sweater", "jumper", "hoodie", 
        "vest", "suit", "tuxedo", "tie", "bowtie", "hat", "cap", "beanie", "helmet", 
        "scarf", "gloves", "mittens", "sock", "socks", "shoe", "shoes", "sneaker", 
        "sneakers", "boot", "boots", "sandal", "sandals", "slipper", "slippers", 
        "glasses", "sunglasses", "spectacles", "watch", "necklace", "bracelet", "ring", 
        "earring", "earrings", "jewelry", "bag", "backpack", "purse", "wallet", 
        "umbrella", "belt", "hairband", "headband", "wig"
    ],
    "Objects": [
        # Catch-all plus specific objects
        "house", "home", "building", "school", "shop", "store", "hut", "tent", "castle",
        "book", "pen", "pencil", "eraser", "ruler", "scissors", "glue", "tape", "paper", 
        "notebook", "folder", "stapler", "clip", "binder", "highlighter", "marker", "crayon",
        "ball", "toy", "doll", "robot", "block", "lego", "kite", "balloon", "game", "puzzle",
        "box", "package", "gift", "present", "ribbon", "bow",
        "camera", "phone", "smartphone", "mobile", "computer", "laptop", "tablet", "screen", 
        "monitor", "tv", "television", "radio", "speaker", "headphone", "earphone", "keyboard", "mouse",
        "instrument", "guitar", "piano", "drum", "violin", "flute", "trumpet", "music",
        "tool", "hammer", "wrench", "screwdriver", "saw", "drill", "axe", "shovel", "rake", "trowel",
        "ladder", "bucket", "dail", "sponge", "broom", "mop", "brush", "comb", "toothbrush", 
        "toothpaste", "soap", "shampoo", "lotion", "towel", "toilet_paper",
        "key", "lock", "coin", "money", "cash", "card", "gem", "diamond", "gold", 
        "star", "moon", "sun", "cloud", "rain", "snow", "fire", "flame", "smoke", 
        "light_bulb", "battery", "plug", "wire",
        "trash", "garbage", "rubbish", "bin", "can"
    ]
}

def organize_files():
    # 1. Create directories
    for category in CATEGORIES.keys():
        dir_path = os.path.join(LIBRARY_DIR, category)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")

    # Objects folder is explicitly in CATEGORIES, so it's created.

    # 2. Scan and Move
    files = [f for f in os.listdir(LIBRARY_DIR) if os.path.isfile(os.path.join(LIBRARY_DIR, f)) and f.lower().endswith('.png')]
    
    moved_count = 0
    misc_count = 0
    
    for fname in files:
        if "batch_preview" in fname:
            continue
            
        lower_name = fname.lower()
        target_category = None
        
        # Priority check
        # Check Characters specifically for actions/roles first
        for key in CATEGORIES["Characters"]:
            if key in lower_name:
                target_category = "Characters"
                break
        
        if not target_category:
            # Check Animals (careful of cooked animals in food)
            for key in CATEGORIES["Animals"]:
                if key in lower_name:
                    # Exception: if it says "cooked", "fried", "roast", "meat" -> Food
                    if any(x in lower_name for x in ["cooked", "fried", "roast", "meat", "food", "dinner"]):
                        target_category = "Food"
                    else:
                        target_category = "Animals"
                    break
                    
        if not target_category:
            # Check Transport
            for key in CATEGORIES["Transport"]:
                if key in lower_name:
                    target_category = "Transport"
                    break
                    
        if not target_category:
            # Check Food
            for key in CATEGORIES["Food"]:
                if key in lower_name:
                    target_category = "Food"
                    break

        if not target_category:
            # Check Plants
            for key in CATEGORIES["Plants"]:
                if key in lower_name:
                    target_category = "Plants"
                    break
                    
        if not target_category:
            # Check Furniture
            for key in CATEGORIES["Furniture"]:
                if key in lower_name:
                    target_category = "Furniture"
                    break
        
        if not target_category:
            # Check Clothes
            for key in CATEGORIES["Clothes"]:
                if key in lower_name:
                    target_category = "Clothes"
                    break
                    
        if not target_category:
            # Check Objects (Specific)
            for key in CATEGORIES["Objects"]:
                if key in lower_name:
                    target_category = "Objects"
                    break

        # Fallback to Objects if generic
        if not target_category:
            target_category = "Objects"

        # Special Overrides
        # "misc_..." -> Objects
        if fname.startswith("misc_"):
            target_category = "Objects"
        if fname.startswith("droplet_"):
            target_category = "Objects"
        if fname.startswith("tobeid_"):
            target_category = "Objects"

        # Move
        src = os.path.join(LIBRARY_DIR, fname)
        dst = os.path.join(LIBRARY_DIR, target_category, fname)
        
        try:
            shutil.move(src, dst)
            # print(f"Moved {fname} -> {target_category}")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {fname}: {e}")

    print(f"Organization Complete. Moved {moved_count} files.")

if __name__ == "__main__":
    organize_files()
