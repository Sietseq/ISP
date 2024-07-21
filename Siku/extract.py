import concurrent.futures
import os
import json
import os
import patoolib
import extract
import os
import re
import sys



def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

holiday_keywords = {
    "general": {
        "keywords": [
            "holiday", "celebration", "festival", "vacation", "holiday season", "festive", 
            "traditions", "party", "gifts", "decorations", "holiday cheer", "family", 
            "friends", "gathering", "holiday spirit", "festivities", "seasonal", "joyful", 
            "holiday sale", "getaway"
        ]
    },
    "christmas": {
        "keywords": [
            "christmas", "xmas", "christmas tree", "santa claus", "presents", "christmas lights", 
            "ornaments", "stockings", "holiday music", "christmas carols", "snow", "winter wonderland", 
            "reindeer", "mistletoe", "gingerbread", "nativity", "elf", "christmas eve", "christmas day", 
            "north pole", "yule", "yuletide", "christmas market", "advent calendar", "christmas card", 
            "christmas dinner", "eggnog", "holly", "tinsel", "wrapping paper", "chimney", "chimney sweep", 
            "rudolph", "winter solstice"
        ]
    },
    "new year": {
        "keywords": [
            "new year", "new year's eve", "new year's day", "countdown", "fireworks", "resolutions", 
            "celebration", "party", "champagne", "midnight", "ball drop", "new beginnings", "toast", 
            "new year’s resolutions", "new year's party", "january 1st", "confetti", "new year’s parade"
        ]
    },
    "halloween": {
        "keywords": [
            "halloween", "spooky", "haunted", "costumes", "trick or treat", "jack-o'-lantern", "ghosts", 
            "witches", "pumpkins", "candy", "monsters", "horror", "bats", "black cat", "frankenstein", 
            "vampires", "werewolves", "zombies", "graveyard", "tombstones", "scarecrow", "witch hat", 
            "cauldron", "halloween party", "haunted house", "mummy", "spiderweb", "spooky decorations", 
            "ghouls", "boo"
        ]
    },
    "thanksgiving": {
        "keywords": [
            "thanksgiving", "turkey", "gratitude", "feast", "family", "harvest", "autumn", "pilgrim", 
            "stuffing", "cranberry sauce", "pumpkin pie", "blessings", "thankful", "cornucopia", 
            "thanksgiving dinner", "thanksgiving parade", "gathering", "mashed potatoes", "gravy", 
            "green bean casserole", "thanksgiving day", "fall leaves", "thanksgiving turkey", 
            "thanksgiving football"
        ]
    },
    "valentine's day": {
        "keywords": [
            "valentine's day", "love", "romance", "hearts", "cupid", "chocolates", "flowers", "roses", 
            "cards", "romantic dinner", "sweetheart", "valentine", "affection", "romantic", "valentine's gift", 
            "red roses", "valentine's card", "love letter", "teddy bear", "proposal", "engagement", 
            "romantic getaway", "valentine's day party"
        ]
    },
    "easter": {
        "keywords": [
            "easter", "bunny", "eggs", "resurrection", "spring", "easter egg hunt", "baskets", "church", 
            "lilies", "good friday", "easter sunday", "easter basket", "easter bunny", "easter parade", 
            "easter bonnet", "chocolate eggs", "easter brunch", "easter lily", "passion week", "holy week", 
            "palm sunday", "maundy thursday", "good friday", "easter vigil", "resurrection sunday", "egg rolling", 
            "egg dyeing"
        ]
    },
    "independence day (usa)": {
        "keywords": [
            "fourth of july", "independence day", "fireworks", "liberty", "patriotism", "america", "bbq", 
            "parade", "stars and stripes", "red, white, and blue", "freedom", "flag", "july 4th", "celebration", 
            "american flag", "picnic", "hot dogs", "hamburgers", "star-spangled banner", "constitution", 
            "declaration of independence", "independence day fireworks", "4th of july barbecue"
        ]
    },
    "hanukkah": {
        "keywords": [
            "hanukkah", "menorah", "dreidel", "latkes", "festival of lights", "jewish holiday", "gelt", 
            "hanukkah candles", "hanukkah gifts", "sufganiyot", "hanukkah songs", "hanukkah traditions", 
            "hanukkah menorah", "shamash", "hanukkah gelt", "hanukkah blessings", "dreidel game", 
            "hanukkah food"
        ]
    },
    "diwali": {
        "keywords": [
            "diwali", "lights", "festival of lights", "hindu festival", "rangoli", "sweets", "diyas", 
            "celebration", "new year", "fireworks", "goddess lakshmi", "prayers", "festive", "diwali gifts", 
            "diwali sweets", "diwali diyas", "diwali decorations", "diwali puja", "diwali festival", 
            "diwali celebration", "happy diwali"
        ]
    },
    "st. patrick's day": {
        "keywords": [
            "st. patrick's day", "shamrock", "irish", "green", "leprechaun", "parade", "luck", "saint patrick", 
            "irish heritage", "st. patrick's day parade", "st. patrick's day party", "green beer", 
            "irish music", "st. patrick's day celebration", "lucky", "four-leaf clover", "pot of gold", 
            "blarney stone", "irish dance", "celtic", "st. patrick's day costume", "irish pub"
        ]
    },
    "mother's day": {
        "keywords": [
            "mother's day", "mom", "mother", "celebration", "appreciation", "flowers", "gift", "love", 
            "breakfast in bed", "mother's day card", "happy mother's day", "mommy", "mother's day brunch", 
            "thank you mom", "special day", "mother's day gift", "mother's day flowers", "mother's day dinner", 
            "mother's day celebration", "super mom", "best mom", "mother's day cake", "family time"
        ]
    },
    "father's day": {
        "keywords": [
            "father's day", "dad", "father", "appreciation", "celebration", "gift", "bbq", "love", 
            "father's day card", "happy father's day", "daddy", "father's day brunch", "thank you dad", 
            "special day", "father's day gift", "father's day dinner", "father's day celebration", 
            "super dad", "best dad", "father's day cake", "family time", "dad's day", "father's day bbq", 
            "tool set", "fishing"
        ]
    }
}

def read_file(f):
    # Open first file
    file = open(f, 'r', encoding="utf8")
    count = {
        "general": {},
        "christmas": {},
        "new year": {},
        "halloween": {},
        "thanksgiving": {},
        "valentine's day": {},
        "easter": {},
        "independence day (usa)": {},
        "hanukkah": {},
        "diwali": {},
        "st. patrick's day": {},
        "mother's day": {},
        "father's day": {}
    }
    while True:
        # Read line
        line = file.readline()
        if not line:
            break

        # Convert metadata into list
        obj = json.loads(line)
        if ('includes' in obj and 'tweets' in obj.get('includes')):
            list = obj.get('includes').get("tweets")
    
        # Go through all tweets
        if (list is not None):
            for tweet in list:
                text = tweet.get("text").lower()
                date = tweet.get("created_at")[:10]
                if (int(date[:4]) > 2019):
                    for category in holiday_keywords:
                        for word in holiday_keywords[category]["keywords"]:
                            if findWholeWord(word)(text) != None :
                                if date in count[category]:
                                    count[category][date] += 1
                                else:
                                    count[category][date] = 1                   
            

    file.close()
    return count

# Prepares everything to be read
def thread_process(f):
    print(f)
    name = os.path.splitext(f)[0]
    base_name = os.path.basename(name)

    count = {}
    if (os.path.splitext(f)[1] == ".json"):
        base_name = os.path.basename(name)
        count = extract.read_file(f)
    else:
        patoolib.extract_archive(f, outdir="./" + str(sys.argv[1]) + "/current", verbosity=-1)
        base_name = os.path.basename(name)
        count = extract.read_file("./" + str(sys.argv[1]) + "/current/" + base_name)
        os.remove("./" + str(sys.argv[1]) + "/current/" + base_name)

    return count


def main():
    # Count variable
    count = {
    "general": {},
    "christmas": {},
    "new year": {},
    "halloween": {},
    "thanksgiving": {},
    "valentine's day": {},
    "easter": {},
    "independence day (usa)": {},
    "hanukkah": {},
    "diwali": {},
    "st. patrick's day": {},
    "mother's day": {},
    "father's day": {}
    }

    # Go through folder
    file_name_list = []
    for dirpath, dirnames, filenames in os.walk("./" + str(sys.argv[1]) + "/extraction"):
        for filename in filenames:
            file_name_list.append(os.path.join(dirpath, filename))

    # Paralel processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for name, dic in zip(file_name_list, executor.map(thread_process, file_name_list)):
            for category in dic:
                dates = list(count[category].keys())
                for date in dic[category]:
                    if date in count[category]:
                        count[category][date] += dic[category][date]
                    else:
                        count[category][date] = dic[category][date]


    # Convert and write JSON object to file
    with open(str(sys.argv[1]) + ".json", "w") as outfile: 
        json.dump(count, outfile)

                     

if __name__ == '__main__':
    main()
