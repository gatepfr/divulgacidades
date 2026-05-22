import json
import requests
import sys

# Load mapped cities
with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

londrina_code = mapped_cities.get("PR", {}).get("LONDRINA")
print(f"Londrina TSE code: {londrina_code}")

if not londrina_code:
    print("Londrina not found in mapped_cities.json.")
    sys.exit(1)

# Fetch Vereador (Cargo 0013) from pleito 619
uf = "pr"
ver_url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{londrina_code}-c0013-e000619-u.json"
print(f"Fetching from: {ver_url}")

r = requests.get(ver_url)
if r.status_code != 200:
    print(f"Failed to fetch data from TSE. Status: {r.status_code}")
    sys.exit(1)

data = r.json()
carg_ver_list = data.get('carg', [])
if not carg_ver_list:
    print("No cargo list found.")
    sys.exit(1)

cargo_ver_data = carg_ver_list[0]
nv = int(cargo_ver_data.get('nv', 0))
print(f"Number of seats (nv): {nv}")

all_cands = []
official_elected = []

for agr in cargo_ver_data.get('agr', []):
    party_sigla = ""
    for par in agr.get('par', []):
        party_sigla = par.get('sg', '')
        for cand in par.get('cand', []):
            dvt = cand.get('dvt', '')
            e_status = cand.get('e', '')
            st_status = cand.get('st', '')
            vaps = cand.get('vap', '0')
            votes = int(vaps) if vaps.isdigit() else 0
            
            cand_info = {
                "nome": cand.get('nm', ''),
                "nomeUrna": cand.get('nmu', ''),
                "partido": party_sigla,
                "numero": cand.get('n', ''),
                "votos": votes,
                "situacao": st_status,
                "e_status": e_status,
                "dvt": dvt
            }
            all_cands.append(cand_info)
            
            # This is how determine_elected_vereadores currently identifies elected candidates
            is_official = e_status == 's' or 'Eleito' in st_status
            if is_official:
                official_elected.append(cand_info)

print(f"Total candidates in JSON: {len(all_cands)}")
print(f"Official elected candidates (according to 'e'=='s' or 'Eleito' in 'st'): {len(official_elected)}")

# Print the official elected list
for idx, c in enumerate(sorted(official_elected, key=lambda x: x['votos'], reverse=True), 1):
    print(f"{idx}. {c['nomeUrna']} ({c['partido']}) - Votos: {c['votos']} - st: {c['situacao']} - e: {c['e_status']}")

# Let's see if there are other candidates with 'Eleito' in st or e_status == 's'
non_elected_official = [c for c in all_cands if c not in official_elected]
print("\nSome other top candidates:")
for idx, c in enumerate(sorted(non_elected_official, key=lambda x: x['votos'], reverse=True)[:10], 1):
    print(f"{idx}. {c['nomeUrna']} ({c['partido']}) - Votos: {c['votos']} - st: {c['situacao']} - e: {c['e_status']} - dvt: {c['dvt']}")
