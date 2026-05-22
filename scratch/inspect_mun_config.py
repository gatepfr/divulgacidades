import json
import requests

url = "https://resultados.tse.jus.br/oficial/ele2022/546/config/mun-e000546-cm.json"
print("Fetching mun-e000546-cm.json...")
r = requests.get(url)
data = r.json()

print("Keys:", list(data.keys()))
print("abr keys:", list(data['abr'][0].keys()) if 'abr' in data and data['abr'] else "no abr")

# Let's inspect São Paulo (SP) entries
if 'abr' in data:
    sp_entries = [entry for entry in data['abr'] if entry.get('cd') == 'SP']
    if sp_entries:
        print("SP Entry sample:")
        # print first few sub-municipalities or zones
        mu_list = sp_entries[0].get('mu', [])
        print(f"Number of municipalities in SP: {len(mu_list)}")
        if mu_list:
            print("First municipality sample:", mu_list[0])
            # Check if there is São Paulo (capital) - code 71072
            sp_cap = [mu for mu in mu_list if mu.get('cd') == '71072']
            if sp_cap:
                print("São Paulo Capital municipality config:", sp_cap[0])
