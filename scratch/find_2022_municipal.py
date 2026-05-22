import requests

# We want to find the URL for the municipal results of São Paulo (71072) for Senator (c0005) in 2022.
# In 2024, the path is:
# /oficial/ele2024/619/dados/sp/sp71072-c0011-e000619-u.json
# In 2022, the pleito is 546 (State) or 544 (Federal).

candidates = [
    # Option 1: pleito 546, election e000546
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000546-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000546-r.json",
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados-simplificados/sp/sp71072-c0005-e000546-r.json",
    
    # Option 2: pleito 546, election e000544 (or other combinations)
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000544-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000544-r.json",
    
    # Option 3: what if the folder inside dados is lowercase, but code is different?
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0005-e000546.json",
    
    # Option 4: Is there a different directory or file for municipal voting in 2022?
    # Let's try Gov (c0003)
    "https://resultados.tse.jus.br/oficial/ele2022/546/dados/sp/sp71072-c0003-e000546-u.json",
    
    # Option 5: Let's try to query the config file `mun-e000546-cm.json` we downloaded and see if it lists URLs or keys.
]

# Also try President c0001 (pleito 544) municipal level
candidates += [
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0001-e000544-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0001-e000544-r.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp71072-c0001-e000544-r.json",
]

for url in candidates:
    r = requests.head(url)
    print(f"URL: {url} -> Status: {r.status_code}")
