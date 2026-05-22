import json
import requests

url = "https://resultados.tse.jus.br/oficial/ele2024/619/dados/pr/pr75353-c0013-e000619-u.json"
r = requests.get(url)
data = r.json()

carg_ver_data = data['carg'][0]
nv = int(carg_ver_data.get('nv', 0))
print(f"Number of seats (nv): {nv}")

all_cands = []
official_elected = []

for agr in carg_ver_data.get('agr', []):
    for par in agr.get('par', []):
        party_sigla = par.get('sg', '')
        for cand in par.get('cand', []):
            vaps = cand.get('vap', '0')
            votes = int(vaps) if vaps.isdigit() else 0
            pvap_str = cand.get('pvap', '0').replace(",", ".")
            percent = float(pvap_str) if pvap_str else 0.0
            
            dvt = cand.get('dvt', '')
            e_status = cand.get('e', '')
            st_status = cand.get('st', '')
            
            cand_info = {
                "nome": cand.get('nm', ''),
                "nomeUrna": cand.get('nmu', ''),
                "partido": party_sigla,
                "numero": cand.get('n', ''),
                "votos": votes,
                "percentual": percent,
                "situacao": st_status,
                "sqcand": cand.get('sqcand', ''),
                "_dvt": dvt,
                "_e": e_status
            }
            
            all_cands.append(cand_info)
            
            is_official = e_status == 's' or 'Eleito' in st_status
            if is_official:
                official_elected.append(cand_info)

print(f"Total candidates: {len(all_cands)}")
print(f"Official elected count: {len(official_elected)}")

if len(official_elected) > 0:
    print("Elected candidates:")
    for idx, c in enumerate(sorted(official_elected, key=lambda x: x['votos'], reverse=True)):
        print(f"{idx+1}: {c['nomeUrna']} ({c['partido']}) - {c['situacao']} - {c['votos']} votes")
else:
    print("No official elected found.")
