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
            cands = par.get('cand', [])
            total_cand_votes = sum(int(c.get('vap', '0')) for c in cands)
            valid_cands = [c for c in cands if c.get('dvt') == 'Válido' or c.get('dvt') == 'Válido (legenda)']
            valid_cand_votes = sum(int(c.get('vap', '0')) for c in valid_cands)
            print(f"Party: {par.get('sg')} ({par.get('n')})")
            print(f"  Candidates count: {len(cands)}")
            print(f"  Valid candidates count: {len(valid_cands)}")
            print(f"  Sum of all candidate votes: {total_cand_votes}")
            print(f"  Sum of valid candidate votes: {valid_cand_votes}")
            print(f"  tvtn (nominal): {par.get('tvtn')}")
            print(f"  tvtl (legenda): {par.get('tvtl')}")
            print(f"  tval (anulado): {par.get('tval')}")
            print(f"  tvan (anulado sub judice): {par.get('tvan')}")
