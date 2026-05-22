import requests

urls = [
    # State-wide simplificados
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0005-e000546-r.json", # Senator
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0006-e000546-r.json", # Dep Federal
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp-c0007-e000546-r.json", # Dep Estadual
    
    # Let's see if municipal-level simplificados exist
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp71072-c0005-e000546-r.json",
    # Or in the dados/ folder
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000546-u.json",
]

for url in urls:
    r = requests.head(url)
    print(f"URL: {url} -> Status: {r.status_code}")
