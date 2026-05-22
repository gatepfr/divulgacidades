import requests
import csv
import json
import re

def get_all_tse_cities():
    url = "https://raw.githubusercontent.com/betafcc/Municipios-Brasileiros-TSE/master/municipios_brasileiros_tse.csv"
    print("Downloading TSE municipal codes CSV...")
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)
    
    tse_map = {}
    for row in reader:
        # csv keys: codigo_tse,uf,nome_municipio,capital,codigo_ibge
        uf = row['uf'].upper().strip()
        name = row['nome_municipio'].strip()
        code = row['codigo_tse'].strip().zfill(5)
        
        if uf not in tse_map:
            tse_map[uf] = {}
        tse_map[uf][name] = code
        
    return tse_map

def update_data_js(estados_cidades):
    print("Updating data.js with all 5,570 cities...")
    with open("data.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Format the dictionary nicely for Javascript
    # Convert Python dict to JSON string
    json_str = json.dumps(estados_cidades, indent=2, ensure_ascii=False)
    
    # We replace "const ESTADOS_CIDADES = { ... };" in data.js
    pattern = r'const ESTADOS_CIDADES = \{.*?\};'
    replacement = f'const ESTADOS_CIDADES = {json_str};'
    
    # Using re.DOTALL to match across lines
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    
    if count == 0:
        print("Error: Could not find ESTADOS_CIDADES object in data.js")
        return False
        
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated data.js!")
    return True

def main():
    tse_map = get_all_tse_cities()
    
    # Sort states alphabetically, and cities within each state alphabetically
    sorted_mapped_cities = {}
    sorted_estados_cidades = {}
    
    total_cities = 0
    for uf in sorted(tse_map.keys()):
        sorted_mapped_cities[uf] = {}
        sorted_estados_cidades[uf] = []
        
        # Sort cities in this state
        for city_name in sorted(tse_map[uf].keys()):
            code = tse_map[uf][city_name]
            sorted_mapped_cities[uf][city_name] = code
            sorted_estados_cidades[uf].append(city_name)
            total_cities += 1
            
    print(f"Mapped {total_cities} cities across {len(sorted_mapped_cities)} states.")
    
    # Save the full mapped_cities.json
    with open("scratch/mapped_cities.json", "w", encoding="utf-8") as f:
        json.dump(sorted_mapped_cities, f, indent=2, ensure_ascii=False)
    print("Saved scratch/mapped_cities.json")
    
    # Update data.js with all mapped cities
    update_data_js(sorted_estados_cidades)

if __name__ == "__main__":
    main()
