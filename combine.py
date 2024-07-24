import os
import sys
import json

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

file_name_list = []
for dirpath, dirnames, filenames in os.walk("./counts"):
    for filename in filenames:
        file_name_list.append(os.path.join(dirpath, filename))

for file in file_name_list:
    with open(file, 'r') as f:
        dic = json.load(f)
        for category in dic:
            dates = list(count[category].keys())
            for date in dic[category]:
                if date in count[category]:
                    count[category][date] += dic[category][date]
                else:
                    count[category][date] = dic[category][date]

with open('data.json', 'w') as f:
    json.dump(count, f)