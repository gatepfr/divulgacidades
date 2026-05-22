import json
import requests

# Load mapped cities
with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped = json.load(f)

tse_code = mapped["PR"]["APUCARANA"]
uf = "pr"
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
r = requests.get(url)
data = r.json()

print("Top-level keys:", list(data.keys()))
print("Status 's':", data.get('s'))
print("Election 'e':", data.get('e'))
print("Votes 'v':", data.get('v'))

carg_list = data.get('carg', [])
if carg_list:
    first_cargo = carg_list[0]
    all_cands = []
    for agr in first_cargo.get('agr', []):
        for par in agr.get('par', []):
            for cand in par.get('cand', []):
                all_cands.append(cand)
    
    # Sort candidates by votes descending
    all_cands.sort(key=lambda x: int(x.get('vap', '0')), reverse=True)
    
    print("\nTop 20 candidates by votes:")
    for idx, cand in enumerate(all_cands[:20]):
        print(f"{idx+1}. {cand.get('nmu')} ({cand.get('partido', cand.get('n'))}) - Votos: {cand.get('vap')} - st: {cand.get('st')} - e: {cand.get('e')}")
        
    print("\nAll unique 'st' values:", set(cand.get('st', '') for cand in all_cands))
    print("All unique 'e' values:", set(cand.get('e', '') for cand in all_cands))
