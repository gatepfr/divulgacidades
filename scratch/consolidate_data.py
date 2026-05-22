import json
import os
import unicodedata
import re
import argparse

# Load mapped cities
with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

def get_city_slug(city_name):
    # Normalize unicode to decompose accents (NFD)
    normalized = unicodedata.normalize('NFD', city_name)
    # Remove accent characters (diacritics)
    no_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    # Convert to lowercase
    lowered = no_accents.lower()
    # Remove any characters that are not a-z, 0-9, spaces, or hyphens
    cleaned = re.sub(r'[^a-z0-9\s-]', '', lowered)
    # Replace spaces and hyphens with single underscore
    slug = re.sub(r'[\s-]+', '_', cleaned.strip())
    return slug

def main():
    parser = argparse.ArgumentParser(description="Consolidate 2024 and 2022 data into city-specific JSON files.")
    parser.add_argument("--uf", help="Comma-separated list of UFs to consolidate (e.g. AC,DF,RR)")
    args = parser.parse_args()

    target_ufs = None
    if args.uf:
        target_ufs = [x.strip().upper() for x in args.uf.split(",")]

    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)

    print("Starting consolidation of 2024 and 2022 data...")

    for uf, cities in mapped_cities.items():
        if target_ufs and uf not in target_ufs:
            continue

        print(f"Consolidating state {uf}...")
        
        # Load 2022 results for this state
        parsed_2022_file = f"scratch/parsed_2022/{uf}_2022.json"
        if not os.path.exists(parsed_2022_file):
            print(f"  Warning: {parsed_2022_file} not found. Skipping state.")
            continue
            
        with open(parsed_2022_file, "r", encoding="utf-8") as f22:
            state_2022_data = json.load(f22)
            
        # Ensure state subdirectory exists in output data directory
        state_dir = os.path.join(out_dir, uf)
        os.makedirs(state_dir, exist_ok=True)
        
        for city_name in cities.keys():
            # Format filename for 2024 data (uses replace(" ", "_"))
            city_dashed = city_name.replace(" ", "_")
            parsed_2024_file = f"scratch/parsed_2024/{uf}_{city_dashed}.json"
            
            if not os.path.exists(parsed_2024_file):
                # If we don't have 2024 data for the city, skip it so frontend falls back to procedural simulation
                continue
                
            with open(parsed_2024_file, "r", encoding="utf-8") as f24:
                city_data = json.load(f24)
                
            # Get 2022 results for this city
            city_2022 = state_2022_data.get(city_name, {})
            
            # Merge 2022 data into city_data
            city_data["senadores"] = city_2022.get("senador", [])
            city_data["deputadosFederais"] = city_2022.get("deputadoFederal", [])
            
            # Handle DF's deputadoDistrital vs other state's deputadoEstadual
            if uf == "DF":
                city_data["deputadosEstaduais"] = city_2022.get("deputadoDistrital", [])
            else:
                city_data["deputadosEstaduais"] = city_2022.get("deputadoEstadual", [])
                
            # Generate the URL-friendly city slug
            city_slug = get_city_slug(city_name)
            
            # Save the consolidated city file
            out_file = os.path.join(state_dir, f"{city_slug}.json")
            with open(out_file, "w", encoding="utf-8") as f_out:
                json.dump(city_data, f_out, indent=2, ensure_ascii=False)
            
        print(f"  Processed cities for state {uf}")

    print("Consolidation finished!")

if __name__ == "__main__":
    main()
