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
    for idx_agr, agr in enumerate(cargo.get('agr', [])):
        for idx_par, par in enumerate(agr.get('par', [])):
            for idx_cand, cand in enumerate(par.get('cand', [])):
                if cand.get('n') == '11123' or 'MOISES' in cand.get('nm', '').upper() or 'MOISES' in cand.get('nmu', '').upper():
                    print(f"Found Moises: {cand.get('nmu')} ({cand.get('n')})")
                    print(f"  Agr index: {idx_agr}, name: {agr.get('com') or agr.get('n')}")
                    print(f"  Par index: {idx_par}, name: {par.get('sg')} ({par.get('n')})")
                    print(f"  Candidate details: {cand}")
