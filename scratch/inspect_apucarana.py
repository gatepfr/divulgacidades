import json
import requests

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped = json.load(f)

# Find Apucarana in PR
tse_code = mapped["PR"]["Apucarana"]
print(f"Apucarana TSE code: {tse_code}")

# Fetch Vereador (Cargo 0013) from pleito 619
uf = "pr"
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
print(f"Fetching from: {url}")
r = requests.get(url)
data = r.json()

# Inspect some candidates
carg_list = data.get('carg', [])
if carg_list:
    print("Found cargos.")
    first_cargo = carg_list[0]
    print(f"Cargo name: {first_cargo.get('nmn')}")
    # Let's count candidates and check their fields
    all_cands = []
    for agr in first_cargo.get('agr', []):
        for par in agr.get('par', []):
            for cand in par.get('cand', []):
                all_cands.append(cand)
    print(f"Total candidates: {len(all_cands)}")
    if all_cands:
        print("Keys of first candidate:", list(all_cands[0].keys()))
        # Print a few samples where there's some status
        print("Sample candidates:")
        for cand in all_cands[:5]:
            print({k: cand.get(k) for k in ['n', 'nm', 'nmu', 'st', 'e', 'vap', 'sit', 's', 'cc'] if k in cand})
        
        # Let's see the unique values of 'st' and 'e' and any other single-character keys
        st_values = set(cand.get('st', '') for cand in all_cands)
        e_values = set(cand.get('e', '') for cand in all_cands)
        print("Unique 'st' values:", st_values)
        print("Unique 'e' values:", e_values)
