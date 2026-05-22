import requests
import json

url = "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0005-e000546-r.json"
r = requests.get(url)
data = r.json()

print("Keys:", list(data.keys()))
print("Total candidates in state:", len(data.get('cand', [])))
if data.get('cand'):
    print("First candidate sample:", data['cand'][0])
