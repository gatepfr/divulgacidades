import json
import math

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped = json.load(f)

tse_code = mapped["PR"]["APUCARANA"]
uf = "pr"
url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-u.json"
import requests
r = requests.get(url)
data = r.json()

carg_list = data.get('carg', [])
if not carg_list:
    print("No cargo found")
    exit()

cargo = carg_list[0]
nv = int(cargo.get('nv'))
print(f"Number of vacancies (nv): {nv}")

# 1. Calculate votes per party
parties = {}
all_candidates = []

for agr in cargo.get('agr', []):
    for par in agr.get('par', []):
        party_sg = par.get('sg')
        party_num = par.get('n')
        # Total votes for party = valid nominal votes + legend votes
        # Let's count legend votes
        tvtl = int(par.get('tvtl', '0'))
        
        # Nominal votes for candidates with dvt == 'Válido' or 'Válido (legenda)'
        nominal_votes = 0
        party_candidates = []
        for cand in par.get('cand', []):
            dvt = cand.get('dvt')
            is_valid = dvt in ['Válido', 'Válido (legenda)']
            vap = int(cand.get('vap', '0'))
            if is_valid:
                nominal_votes += vap
            
            cand_info = {
                "nome": cand.get('nm'),
                "nomeUrna": cand.get('nmu'),
                "partido": party_sg,
                "numero": cand.get('n'),
                "votos": vap,
                "dvt": dvt,
                "is_valid": is_valid,
                "sqcand": cand.get('sqcand'),
                "e": cand.get('e'),
                "st": cand.get('st')
            }
            party_candidates.append(cand_info)
            all_candidates.append(cand_info)
            
        total_party_votes = nominal_votes + tvtl
        parties[party_sg] = {
            "sg": party_sg,
            "num": party_num,
            "votes": total_party_votes,
            "candidates": sorted(party_candidates, key=lambda x: x["votos"], reverse=True),
            "seats": 0
        }

# Total valid votes in the city
total_valid_votes = sum(p["votes"] for p in parties.values())
print(f"Total Valid Votes: {total_valid_votes}")

# Quociente Eleitoral (QE)
qe = round(total_valid_votes / nv) # or math.floor? Usually in Brazil it is rounded to the nearest integer, half up, but wait: QE = round(total_valid_votes / nv)
# Actually: QE = total_valid_votes // nv (integer division). If QE < 1, QE = 1.
qe_floor = total_valid_votes // nv
print(f"QE (floor): {qe_floor}")

# Calculate Quociente Partidário (QP) for each party
seats_allocated = 0
for sg, p in parties.items():
    qp = p["votes"] // qe_floor
    p["seats"] = qp
    seats_allocated += qp
    if qp > 0:
        print(f"Party {sg} got {qp} seats directly (votes: {p['votes']})")

remaining_seats = nv - seats_allocated
print(f"Seats allocated directly: {seats_allocated}. Remaining seats (sobras): {remaining_seats}")

# Sobras calculation (leftovers)
# In 2024, the leftover rules are:
# 1st round: highest average among parties that have at least 80% of QE and candidates with at least 20% of QE.
# Let's calculate the average for each party: average = party_votes / (seats_allocated + 1)
for round_num in range(remaining_seats):
    best_party = None
    best_avg = -1
    for sg, p in parties.items():
        # Check if party has enough candidates to fill another seat
        allocated_candidates = [c for c in p["candidates"] if c["is_valid"]]
        if len(allocated_candidates) <= p["seats"]:
            continue
            
        # Average formula: total_votes / (seats + 1)
        avg = p["votes"] / (p["seats"] + 1)
        if avg > best_avg:
            best_avg = avg
            best_party = p
            
    if best_party:
        best_party["seats"] += 1
        print(f"Seat {round_num + 1} of leftovers allocated to {best_party['sg']} (new total: {best_party['seats']}, average: {best_avg:.2f})")

# Print elected candidates per party
elected_candidates = []
for sg, p in parties.items():
    valid_cands = [c for c in p["candidates"] if c["is_valid"]]
    for i in range(min(p["seats"], len(valid_cands))):
        elected_candidates.append(valid_cands[i])

print("\nElected candidates:")
elected_candidates.sort(key=lambda x: x["votos"], reverse=True)
for idx, c in enumerate(elected_candidates):
    print(f"{idx+1}. {c['nomeUrna']} ({c['partido']}) - Votos: {c['votos']}")
