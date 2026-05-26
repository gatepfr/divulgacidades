import json
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load mapped cities
with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

# Output directory for temporary parsed 2024 data
os.makedirs("scratch/parsed_2024", exist_ok=True)

# Helper function to request with retries using a connection pool
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=24, pool_maxsize=24)
session.mount('https://', adapter)

def get_json(url):
    for i in range(5):  # increase retries to 5
        try:
            r = session.get(url, timeout=10)
            if r.status_code == 200:
                # Force UTF-8 if not set
                if r.encoding is None or r.encoding.lower() == 'iso-8859-1':
                    r.encoding = 'utf-8'
                return r.json(), 200
            elif r.status_code == 404:
                return None, 404
            elif r.status_code == 429:
                # Rate limited. Back off exponentially.
                time.sleep(2 * (i + 1))
            else:
                # Other status codes (5xx, etc.)
                time.sleep(1)
        except Exception as e:
            time.sleep(0.5 * (i + 1))
    return None, 500

def determine_elected_vereadores(cargo_ver_data):
    nv = int(cargo_ver_data.get('nv', 0))
    if nv <= 0:
        return []
        
    all_cands = []
    official_elected = []
    
    for agr in cargo_ver_data.get('agr', []):
        coalition_name = agr.get('com', '')
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
                    
    if len(official_elected) > 0:
        all_cands.sort(key=lambda x: x['votos'], reverse=True)
        for c in all_cands:
            c.pop('_dvt', None)
            c.pop('_e', None)
        return all_cands

        
    # Fallback to local proportional representation calculation
    agrs = {}
    for agr in cargo_ver_data.get('agr', []):
        agr_id = agr.get('n')
        agr_name = agr.get('nm')
        agr_com = agr.get('com')
        
        total_legend_votes = 0
        agr_cands = []
        
        for par in agr.get('par', []):
            party_sg = par.get('sg')
            tvtl = int(par.get('tvtl', '0'))
            total_legend_votes += tvtl
            
            for cand in par.get('cand', []):
                vaps = cand.get('vap', '0')
                votes = int(vaps) if vaps.isdigit() else 0
                pvap_str = cand.get('pvap', '0').replace(",", ".")
                percent = float(pvap_str) if pvap_str else 0.0
                
                dvt = cand.get('dvt', '')
                is_valid = dvt == 'Válido' or (dvt.startswith('V') and 'legenda' not in dvt.lower())
                contributes_to_party = dvt.startswith('V')
                
                cand_info = {
                    "nome": cand.get('nm', ''),
                    "nomeUrna": cand.get('nmu', ''),
                    "partido": party_sg,
                    "numero": cand.get('n', ''),
                    "votos": votes,
                    "percentual": percent,
                    "situacao": cand.get('st', ''),
                    "sqcand": cand.get('sqcand', ''),
                    "_is_valid": is_valid,
                    "_contributes": contributes_to_party
                }
                agr_cands.append(cand_info)
                
        nominal_valid_votes = sum(c['votos'] for c in agr_cands if c['_contributes'])
        total_votes = nominal_valid_votes + total_legend_votes
        
        agrs[agr_id] = {
            'id': agr_id,
            'name': agr_name,
            'com': agr_com,
            'votes': total_votes,
            'candidates': sorted(agr_cands, key=lambda x: x['votos'], reverse=True),
            'seats': 0,
            'allocated_candidates': []
        }
        
    total_valid_votes = sum(a['votes'] for a in agrs.values())
    if total_valid_votes == 0:
        return []
        
    ratio = total_valid_votes / nv
    qe = int(ratio)
    if ratio - qe > 0.5:
        qe += 1
    if qe < 1:
        qe = 1
        
    seats_allocated = 0
    for agr_id, a in agrs.items():
        qp = a['votes'] // qe
        valid_cands_above_barrier = [c for c in a['candidates'] if c['_is_valid'] and c['votos'] >= 0.10 * qe]
        qp_allocated = min(qp, len(valid_cands_above_barrier))
        a['seats'] = qp_allocated
        seats_allocated += qp_allocated
        
        for i in range(qp_allocated):
            cand = valid_cands_above_barrier[i]
            cand['situacao'] = "Eleito por QP"
            a['allocated_candidates'].append(cand)
            
    remaining = nv - seats_allocated
    for round_num in range(remaining):
        best_agr = None
        best_avg = -1
        for agr_id, a in agrs.items():
            allocated_names = {c['nomeUrna'] for c in a['allocated_candidates']}
            valid_cands_remaining = [c for c in a['candidates'] if c['_is_valid'] and c['nomeUrna'] not in allocated_names]
            if not valid_cands_remaining:
                continue
            
            avg = a['votes'] / (a['seats'] + 1)
            if avg > best_avg:
                best_avg = avg
                best_agr = a
                
        if best_agr:
            best_agr['seats'] += 1
            allocated_names = {c['nomeUrna'] for c in best_agr['allocated_candidates']}
            valid_cands_remaining = [c for c in best_agr['candidates'] if c['_is_valid'] and c['nomeUrna'] not in allocated_names]
            if valid_cands_remaining:
                cand = valid_cands_remaining[0]
                cand['situacao'] = "Eleito por média"
                best_agr['allocated_candidates'].append(cand)
                
    elected = []
    for agr_id, a in agrs.items():
        elected.extend(a['allocated_candidates'])
        
    elected_map = {c['sqcand']: c['situacao'] for c in elected}
    
    for c in all_cands:
        if c['sqcand'] in elected_map:
            c['situacao'] = elected_map[c['sqcand']]
        else:
            if not c.get('situacao'):
                c['situacao'] = "Suplente" if c['votos'] > 0 else "Não eleito"
                
    all_cands.sort(key=lambda x: x['votos'], reverse=True)
    for c in all_cands:
        c.pop('_dvt', None)
        c.pop('_e', None)
        c.pop('_is_valid', None)
        c.pop('_contributes', None)
        
    return all_cands

def process_city(uf, city_name, tse_code):
    uf_lower = uf.lower()
    out_file = f"scratch/parsed_2024/{uf}_{city_name.replace(' ', '_')}.json"


    if uf == "DF":
        # Brasília has no municipal elections in 2024
        # We write an empty template to avoid errors
        city_result = {
            "populacao": 0,
            "votosValidos": 0,
            "abstencao": 0.0,
            "prefeito": None,
            "vereadores": []
        }
        with open(out_file, "w", encoding="utf-8") as f_out:
            json.dump(city_result, f_out, indent=2, ensure_ascii=False)
        return f"Brasília - DF: Skipped 2024 (Federal District)"

    # 1. Fetch Prefeito (Cargo 0011)
    # Try pleito 620 (second turn) first
    pref_url_620 = f"https://resultados.tse.jus.br/oficial/ele2024/620/dados/{uf_lower}/{uf_lower}{tse_code}-c0011-e000620-u.json"
    pref_data, status = get_json(pref_url_620)
    
    if status == 404 or pref_data is None:
        # Fall back to pleito 619 (first turn)
        pref_url_619 = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf_lower}/{uf_lower}{tse_code}-c0011-e000619-u.json"
        pref_data, status = get_json(pref_url_619)
        if status != 200 or pref_data is None:
            return f"{city_name} - {uf}: FAILED to fetch Prefeito (status {status})"
    
    # 2. Fetch Vereador (Cargo 0013) from pleito 619
    ver_url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf_lower}/{uf_lower}{tse_code}-c0013-e000619-u.json"
    ver_data, status_ver = get_json(ver_url)
    if status_ver != 200 or ver_data is None:
        return f"{city_name} - {uf}: FAILED to fetch Vereador (status {status_ver})"
        
    # Parse Prefeito
    try:
        # Stats
        electorate = int(pref_data.get('e', {}).get('te', 0))
        valid_votes = int(pref_data.get('v', {}).get('vvc', 0))
        abstention_pct = float(pref_data.get('e', {}).get('pa', "0").replace(",", "."))
        
        # Find candidates
        candidates = []
        carg_list = pref_data.get('carg', [])
        if carg_list:
            for agr in carg_list[0].get('agr', []):
                coalition_name = agr.get('com', '')
                for par in agr.get('par', []):
                    party_sigla = par.get('sg', '')
                    for cand in par.get('cand', []):
                        # Check validity
                        if cand.get('dvt') != 'Válido' and cand.get('vap') == '0':
                            continue
                        
                        vaps = cand.get('vap', '0')
                        votes = int(vaps) if vaps.isdigit() else 0
                        
                        pvap_str = cand.get('pvap', '0').replace(",", ".")
                        percent = float(pvap_str) if pvap_str else 0.0
                        
                        vice_list = cand.get('vs', [])
                        vice_name = ""
                        vice_nmu = ""
                        vice_party = ""
                        vice_sqcand = ""
                        if vice_list:
                            vice_name = vice_list[0].get('nm', '')
                            vice_nmu = vice_list[0].get('nmu', '')
                            vice_party = vice_list[0].get('sgp', '')
                            vice_sqcand = vice_list[0].get('sqcand', '')
                            
                        candidates.append({
                            "nome": cand.get('nm', ''),
                            "nomeUrna": cand.get('nmu', ''),
                            "partido": party_sigla,
                            "numero": cand.get('n', ''),
                            "votos": votes,
                            "percentual": percent,
                            "situacao": cand.get('st', ''),
                            "sqcand": cand.get('sqcand', ''),
                            "vice": vice_name,
                            "viceNomeUrna": vice_nmu,
                            "partidoVice": vice_party,
                            "sqcandVice": vice_sqcand,
                            "coligacao": coalition_name
                        })
        
        # Sort candidates by votes descending
        candidates.sort(key=lambda x: x['votos'], reverse=True)
        prefeito_winner = candidates[0] if candidates else None
        
        # Parse Vereadores
        carg_ver_list = ver_data.get('carg', [])
        vereadores = []
        if carg_ver_list:
            vereadores = determine_elected_vereadores(carg_ver_list[0])
            
        if not vereadores and carg_ver_list:
            # Fallback to top 20 by votes
            for agr in carg_ver_list[0].get('agr', []):
                for par in agr.get('par', []):
                    party_sigla = par.get('sg', '')
                    for cand in par.get('cand', []):
                        vaps = cand.get('vap', '0')
                        votes = int(vaps) if vaps.isdigit() else 0
                        
                        pvap_str = cand.get('pvap', '0').replace(",", ".")
                        percent = float(pvap_str) if pvap_str else 0.0
                        
                        vereadores.append({
                            "nome": cand.get('nm', ''),
                            "nomeUrna": cand.get('nmu', ''),
                            "partido": party_sigla,
                            "numero": cand.get('n', ''),
                            "votos": votes,
                            "percentual": percent,
                            "situacao": cand.get('st', ''),
                            "sqcand": cand.get('sqcand', '')
                        })
            vereadores.sort(key=lambda x: x['votos'], reverse=True)

        
        city_result = {
            "populacao": electorate, # using electorate as proxy for size
            "votosValidos": valid_votes,
            "abstencao": abstention_pct,
            "prefeito": prefeito_winner,
            "vereadores": vereadores
        }
        
        with open(out_file, "w", encoding="utf-8") as f_out:
            json.dump(city_result, f_out, indent=2, ensure_ascii=False)
            
        return f"{city_name} - {uf}: Success"
    except Exception as ex:
        return f"{city_name} - {uf}: ERROR parsing: {ex}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch 2024 election data from TSE CDN.")
    parser.add_argument("--uf", help="Comma-separated list of UFs to fetch (e.g. AC,DF,RR)")
    args = parser.parse_args()

    target_ufs = None
    if args.uf:
        target_ufs = [x.strip().upper() for x in args.uf.split(",")]

    tasks = []
    for uf, cities in mapped_cities.items():
        if target_ufs and uf not in target_ufs:
            continue
        for city_name, tse_code in cities.items():
            tasks.append((uf, city_name, tse_code))

    print(f"Starting 2024 TSE results fetch concurrently for {len(tasks)} cities...")
    
    if len(tasks) == 0:
        print("No cities to fetch.")
        return

    # Run with 16 parallel threads using connection pool to maximize speed safely
    completed = 0
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(process_city, uf, city_name, tse_code): (city_name, uf) for uf, city_name, tse_code in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            print(f"[{completed}/{len(tasks)}] {res}")

if __name__ == "__main__":
    main()
