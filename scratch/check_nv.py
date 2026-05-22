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
    print(f"Cargo: {cargo.get('nmn')}")
    print(f"nv (Number of vacancies): {cargo.get('nv')}")
