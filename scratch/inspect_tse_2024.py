import requests
import json

url = "https://resultados.tse.jus.br/oficial/ele2024/619/dados/sp/sp71072-c0011-e000619-u.json"
response = requests.get(url)
data = response.json()

# Save a pretty-printed version of the first few levels of the JSON to understand it
with open("scratch/sample_prefeito_sp.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved sample Prefeito JSON. Checking structure...")
print("Top-level keys:", list(data.keys()))
if 't' in data:
    print("Keys under 't':", list(data['t'].keys()))
    # Let's see some details
    print("candidatos in 't':", type(data['t'].get('cands', [])))
    cands = data['t'].get('cands', [])
    print("Number of candidates:", len(cands))
    if cands:
        print("First candidate sample keys:", list(cands[0].keys()))
        print("First candidate sample:", {k: cands[0][k] for k in ['n', 'nm', 'nv', 'v', 'pvap', 'cc'] if k in cands[0]})
