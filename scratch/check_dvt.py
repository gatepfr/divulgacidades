import json
import requests

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped = json.load(f)

tse_code = mapped["PR"]["APUCARANA"]
uf = "pr"
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
r = requests.get(url)
data = r.json()

carg_list = data.get('carg', [])
if carg_list:
    cargo = carg_list[0]
    all_cands = []
    for agr in cargo.get('agr', []):
        for par in agr.get('par', []):
            for cand in par.get('cand', []):
                all_cands.append(cand)
    
    # Sort candidates by votes descending
    all_cands.sort(key=lambda x: int(x.get('vap', '0')), reverse=True)
    
    print("Top 20 candidates in Apucarana with 'dvt' and other keys:")
    for idx, cand in enumerate(all_cands[:20]):
        print(f"{idx+1}. {cand.get('nmu')} ({cand.get('partido', cand.get('n'))}) - Votos: {cand.get('vap')} - dvt: {cand.get('dvt')} - st: {cand.get('st')} - e: {cand.get('e')}")
