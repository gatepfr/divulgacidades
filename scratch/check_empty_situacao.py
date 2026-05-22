import os
import json

empty_cities = []
total_cities = 0
df_cities = 0

for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith(".json"):
            total_cities += 1
            path = os.path.join(root, file)
            state = os.path.basename(root)
            
            if state == "DF":
                df_cities += 1
                continue
                
            try:
                with open(path, "r", encoding="utf-8") as f:
                    city_data = json.load(f)
                
                vereadores = city_data.get("vereadores", [])
                if not vereadores:
                    # Some cities might not have vereadores if they failed or if it's DF
                    continue
                    
                # Check if all vereadores have empty situacao
                all_empty = all(v.get("situacao", "") == "" for v in vereadores)
                # Or check if no vereador has a status indicating election ("Eleito", "Eleito por QP", "Eleito por média")
                has_any_elected = any("Eleito" in v.get("situacao", "") for v in vereadores)
                
                if all_empty or not has_any_elected:
                    empty_cities.append((state, file, all_empty, has_any_elected))
            except Exception as e:
                print(f"Error reading {path}: {e}")

print(f"Total cities checked: {total_cities} (DF: {df_cities})")
print(f"Cities with empty or no elected status for vereadores: {len(empty_cities)}")
print("Sample of empty cities (up to 20):")
for item in empty_cities[:20]:
    print(f"State: {item[0]}, File: {item[1]}, All Empty: {item[2]}, Has Any Elected: {item[3]}")
