import requests

uf = "sp"
tse_code = "71072" # Sao Paulo
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
r = requests.get(url)
data = r.json()

carg_list = data.get('carg', [])
if carg_list:
    first_cargo = carg_list[0]
    all_cands = []
    for agr in first_cargo.get('agr', []):
        for par in agr.get('par', []):
            for cand in par.get('cand', []):
                all_cands.append(cand)
    
    print(f"Total candidates in SP: {len(all_cands)}")
    st_values = set(cand.get('st', '') for cand in all_cands)
    e_values = set(cand.get('e', '') for cand in all_cands)
    print("Unique 'st' values:", st_values)
    print("Unique 'e' values:", e_values)
    
    # Sort candidates by votes descending
    all_cands.sort(key=lambda x: int(x.get('vap', '0')), reverse=True)
    
    print("\nTop 10 candidates by votes in SP:")
    for idx, cand in enumerate(all_cands[:10]):
        print(f"{idx+1}. {cand.get('nmu')} ({cand.get('partido', cand.get('n'))}) - Votos: {cand.get('vap')} - st: {cand.get('st')} - e: {cand.get('e')}")
