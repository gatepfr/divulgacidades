import json
import os
import zipfile
import csv
import io

# Load mapped cities
with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

zip_path = "scratch/votacao_candidato_munzona_2022.zip"
out_dir = "scratch/parsed_2022"
os.makedirs(out_dir, exist_ok=True)

print("Starting 2022 TSE results processing...")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for uf, cities in mapped_cities.items():
        print(f"Processing state {uf}...")
        csv_name = f"votacao_candidato_munzona_2022_{uf}.csv"
        
        # Check if the CSV exists inside the ZIP
        if csv_name not in zip_ref.namelist():
            print(f"  Warning: {csv_name} not found in ZIP. Skipping.")
            continue
            
        # Target codes for this state
        target_codes = set(cities.values())
        
        # Determine state deputy cargo code (7 for states, 8 for DF)
        state_deputy_cargo = 8 if uf == "DF" else 7
        target_cargos = {5, 6, state_deputy_cargo}
        
        # Data structures
        candidates_votes = {} # tse_code -> cargo -> sq_candidato -> votes
        candidates_meta = {}  # sq_candidato -> {name, name_urna, party, number}
        cargo_total_votes = {} # tse_code -> cargo -> total_votes
        
        for code in target_codes:
            candidates_votes[code] = {5: {}, 6: {}, state_deputy_cargo: {}}
            cargo_total_votes[code] = {5: 0, 6: 0, state_deputy_cargo: 0}
            
        # Open CSV entry
        with zip_ref.open(csv_name) as f_bin:
            f_text = io.TextIOWrapper(f_bin, encoding='latin1')
            reader = csv.reader(f_text, delimiter=';')
            try:
                header = next(reader)
            except StopIteration:
                print(f"  Empty CSV file: {csv_name}")
                continue
                
            # Process line by line
            line_count = 0
            for row in reader:
                line_count += 1
                if line_count % 1000000 == 0:
                    print(f"  Read {line_count} lines...")
                    
                if len(row) < 50:
                    continue
                    
                tse_code = row[13].zfill(5)
                if tse_code not in target_codes:
                    continue
                    
                try:
                    turno = int(row[5])
                except ValueError:
                    continue
                if turno != 1:
                    continue
                    
                try:
                    cargo = int(row[16])
                except ValueError:
                    continue
                if cargo not in target_cargos:
                    continue
                    
                sq_cand = row[18]
                num_cand = row[19]
                name_cand = row[20]
                name_urna = row[21]
                party = row[35]
                
                try:
                    votes = int(row[45])
                except ValueError:
                    votes = 0
                    
                if votes <= 0:
                    continue
                    
                # Accumulate
                candidates_votes[tse_code][cargo][sq_cand] = candidates_votes[tse_code][cargo].get(sq_cand, 0) + votes
                cargo_total_votes[tse_code][cargo] += votes
                
                # Store metadata
                candidates_meta[sq_cand] = {
                    "nome": name_cand,
                    "nomeUrna": name_urna,
                    "partido": party,
                    "numero": num_cand,
                    "sqcand": sq_cand
                }
                
        # Aggregate results for each city in this state
        state_results = {}
        for city_name, code in cities.items():
            city_results = {}
            for cargo in target_cargos:
                cargo_label = "senador" if cargo == 5 else ("deputadoFederal" if cargo == 6 else "deputadoEstadual")
                if uf == "DF" and cargo == 8:
                    cargo_label = "deputadoDistrital"
                    
                total_votes = cargo_total_votes[code][cargo]
                
                # Get candidates list
                cand_list = []
                for sq_cand, votes in candidates_votes[code][cargo].items():
                    meta = candidates_meta[sq_cand]
                    pct = (votes / total_votes * 100) if total_votes > 0 else 0.0
                    cand_list.append({
                        "nome": meta["nome"],
                        "nomeUrna": meta["nomeUrna"],
                        "partido": meta["partido"],
                        "numero": meta["numero"],
                        "votos": votes,
                        "percentual": round(pct, 2),
                        "sqcand": meta["sqcand"]
                    })
                    
                # Sort by votes descending
                cand_list.sort(key=lambda x: x["votos"], reverse=True)
                
                # Keep top 3 for Senator, top 7 for Federal/State/District Deputies
                limit = 3 if cargo == 5 else 7
                city_results[cargo_label] = cand_list[:limit]
                
            state_results[city_name] = city_results
            
        # Write state parsed 2022 results
        out_file = os.path.join(out_dir, f"{uf}_2022.json")
        with open(out_file, "w", encoding="utf-8") as f_out:
            json.dump(state_results, f_out, indent=2, ensure_ascii=False)
            
        print(f"Finished processing state {uf}. Output saved to {out_file}.")

print("2022 TSE results processing finished!")
