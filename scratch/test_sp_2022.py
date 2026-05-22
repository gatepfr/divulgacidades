import requests

paths = [
    # Try different state codes and cases
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0003-e000544-r.json", # Gov SP
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0001-e000544-r.json", # Pres SP
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0005-e000544-r.json", # Senator SP
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0003-e000544-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0005-e000544-u.json",
    
    # Try with uppercase SP
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/SP/SP-c0003-e000544-r.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/SP-c0003-e000544-r.json",
]

for url in paths:
    r = requests.head(url)
    print(f"URL: {url} -> Status: {r.status_code}")
