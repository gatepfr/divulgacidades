import requests
import json

r = requests.get('https://resultados.tse.jus.br/oficial/ele2024/619/dados/pr/pr74250-c0013-e000619-u.json')
data = r.json()
cargo = data['carg'][0]
nv = 11

agrs = {}
for agr in cargo.get('agr', []):
    agr_id = agr.get('n')
    agr_name = agr.get('nm')
    agr_com = agr.get('com')
    
    total_legend_votes = 0
    all_cands = []
    
    for par in agr.get('par', []):
        party_sg = par.get('sg')
        tvtl = int(par.get('tvtl', '0'))
        total_legend_votes += tvtl
        
        for cand in par.get('cand', []):
            vap = int(cand.get('vap', '0'))
            dvt = cand.get('dvt')
            # Normalize dvt
            is_valid = dvt == 'Válido' or dvt.startswith('V') and 'legenda' not in dvt
            contributes_to_party = dvt.startswith('V')
            
            all_cands.append({
                'nomeUrna': cand.get('nmu'),
                'sg': party_sg,
                'votos': vap,
                'is_valid': is_valid,
                'contributes': contributes_to_party,
                'dvt': dvt
            })
            
    # Calculate total votes for this AGR
    nominal_valid_votes = sum(c['votos'] for c in all_cands if c['contributes'])
    total_votes = nominal_valid_votes + total_legend_votes
    
    agrs[agr_id] = {
        'id': agr_id,
        'name': agr_name,
        'com': agr_com,
        'votes': total_votes,
        'candidates': sorted(all_cands, key=lambda x: x['votos'], reverse=True),
        'seats': 0
    }

total_valid_votes = sum(a['votes'] for a in agrs.values())
print('Total Valid Votes:', total_valid_votes)

ratio = total_valid_votes / nv
fraction = ratio - (total_valid_votes // nv)
if fraction > 0.5:
    qe = (total_valid_votes // nv) + 1
else:
    qe = total_valid_votes // nv
if qe < 1:
    qe = 1
print('QE calculated:', qe)

# Direct seats (QP)
seats_allocated = 0
for agr_id, a in agrs.items():
    qp = a['votes'] // qe
    valid_cands_above_barrier = [c for c in a['candidates'] if c['is_valid'] and c['votos'] >= 0.10 * qe]
    qp_allocated = min(qp, len(valid_cands_above_barrier))
    a['seats'] = qp_allocated
    seats_allocated += qp_allocated
    if qp_allocated > 0:
        print(f"AGR {a['com']} got {qp_allocated} seats directly (votes: {a['votes']}, QP: {qp})")

# Sobras (leftovers)
remaining = nv - seats_allocated
print(f"Direct seats: {seats_allocated}. Leftover seats: {remaining}")
for round_num in range(remaining):
    best_agr = None
    best_avg = -1
    for agr_id, a in agrs.items():
        # AGR must have eligible candidates who are valid and not yet allocated
        valid_cands_remaining = [c for c in a['candidates'] if c['is_valid']]
        if len(valid_cands_remaining) <= a['seats']:
            continue
        avg = a['votes'] / (a['seats'] + 1)
        if avg > best_avg:
            best_avg = avg
            best_agr = a
    if best_agr:
        best_agr['seats'] += 1
        print(f"Leftover round {round_num+1} allocated to {best_agr['com']} (new total: {best_agr['seats']}, average: {best_avg:.2f})")

# Elected candidates list
elected = []
for agr_id, a in agrs.items():
    valid_cands = [c for c in a['candidates'] if c['is_valid']]
    for i in range(min(a['seats'], len(valid_cands))):
        elected.append(valid_cands[i])

elected.sort(key=lambda x: x['votos'], reverse=True)
print("\nElected candidates:")
for idx, c in enumerate(elected):
    print(f"{idx+1}. {c['nomeUrna']} ({c['sg']}) - Votos: {c['votos']} - dvt: {c['dvt']}")
