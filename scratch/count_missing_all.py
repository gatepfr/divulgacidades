import os
import json

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

total_missing = 0
total_cities = 0

for uf, cities in mapped_cities.items():
    missing_count = 0
    for city in cities:
        file_name = f"{uf}_{city.replace(' ', '_')}.json"
        path = f"scratch/parsed_2024/{file_name}"
        if not os.path.exists(path):
            missing_count += 1
            
    total_cities += len(cities)
    total_missing += missing_count
    if missing_count > 0:
        print(f"UF {uf}: {missing_count} missing out of {len(cities)}")

print(f"\nTotal cities: {total_cities}")
print(f"Total missing: {total_missing}")
