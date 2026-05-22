import os
import json

directory = "scratch/parsed_2024"
if not os.path.exists(directory):
    print("Directory does not exist.")
    exit(1)

buggy_count = 0
total_count = 0
df_count = 0
situations = set()

buggy_files = []

for filename in os.listdir(directory):
    if not filename.endswith(".json"):
        continue
    total_count += 1
    filepath = os.path.join(directory, filename)
    
    if filename == "DF_Brasília.json":
        df_count += 1
        continue
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        vereadores = data.get("vereadores", [])
        is_buggy = False
        
        # If there are candidates who are not elected (e.g. Suplente, Não eleito, etc.)
        for v in vereadores:
            sit = v.get("situacao", "")
            situations.add(sit)
            # Check if any candidate has a non-elected situation
            # Usually, elected will contain "eleito" (Eleito, Eleito por QP, Eleito por média)
            if "eleito" not in sit.lower():
                is_buggy = True
                
        # Also check if it's exactly 20 and we have a suspicion
        if is_buggy:
            buggy_count += 1
            buggy_files.append(filename)
            
    except Exception as e:
        print(f"Error reading {filename}: {e}")

print(f"Total files: {total_count}")
print(f"DF files: {df_count}")
print(f"Buggy files (containing non-elected): {buggy_count}")
print(f"Unique situations found: {sorted(list(situations))}")
if buggy_files:
    print(f"Sample buggy files: {buggy_files[:10]}")
