import json
import requests

tse_code = "74136"
uf = "pr"
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
r = requests.get(url)
data = r.json()

carg_list = data.get('carg', [])
if carg_list:
    cargo = carg_list[0]
    for agr in cargo.get('agr', []):
        for par in agr.get('par', []):
            if par.get('sg') == 'PP':
                print(f"Found PP in agr {agr.get('com') or agr.get('n')}:")
                for cand in par.get('cand', []):
                    print(f"  Candidate: {cand.get('nmu')} ({cand.get('n')}) - Votos: {cand.get('vap')} - dvt: {cand.get('dvt')}")
