import os
import json

directory = "scratch/parsed_2024"
if not os.path.exists(directory):
    print("Directory does not exist.")
    exit(1)

deleted_count = 0
total_count = 0

for filename in os.listdir(directory):
    if not filename.endswith(".json"):
        continue
    total_count += 1
    filepath = os.path.join(directory, filename)
    
    if filename == "DF_Brasília.json":
        continue
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        vereadores = data.get("vereadores", [])
        
        # If the vereadores list is empty, it needs to be re-fetched (except DF)
        if not vereadores:
            print(f"Deleting {filename} (empty vereadores list)")
            os.remove(filepath)
            deleted_count += 1
            continue
            
        is_buggy = False
        for v in vereadores:
            sit = v.get("situacao", "")
            # Check if there is any candidate whose status is NOT "eleito" (e.g. Suplente, Não eleito, etc.)
            if "eleito" not in sit.lower():
                is_buggy = True
                break
                
        if is_buggy:
            os.remove(filepath)
            deleted_count += 1
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print(f"Scanned {total_count} files.")
print(f"Deleted {deleted_count} files containing buggy or incomplete data.")
