import os
import json

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped = json.load(f)["AC"]

missing = []
for city in mapped:
    file_name = f"AC_{city.replace(' ', '_')}.json"
    path = f"scratch/parsed_2024/{file_name}"
    if not os.path.exists(path):
        missing.append(city)

print(f"Missing cities for AC: {len(missing)} out of {len(mapped)}")
print(f"List: {missing}")
