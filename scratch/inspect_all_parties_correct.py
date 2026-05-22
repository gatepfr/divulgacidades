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
    print(f"Vacancies (nv): {cargo.get('nv')}")
    for idx, agr in enumerate(cargo.get('agr', [])):
        print(f"\nAgremiação: {agr.get('com') or agr.get('n')}")
        for par in agr.get('par', []):
            cands = par.get('cand', [])
            total_votes = sum(int(c.get('vap', '0')) for c in cands)
            print(f"  Party: {par.get('sg')} ({par.get('n')})")
            print(f"    Candidates count: {len(cands)}")
            print(f"    Sum candidate votes: {total_votes}")
            print(f"    tvtn (nominal): {par.get('tvtn')}")
            print(f"    tvtl (legenda): {par.get('tvtl')}")
            print(f"    tval (anulado): {par.get('tval')}")
            print(f"    tvan (anulado sub judice): {par.get('tvan')}")
            if cands:
                for cand in cands[:2]:
                    print(f"    Candidate: {cand.get('nmu')} ({cand.get('n')}) - {cand.get('vap')} votes - dvt: {cand.get('dvt')} - st: {cand.get('st')} - e: {cand.get('e')}")
            else:
                print("    No candidates")
