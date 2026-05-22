import requests

urls = [
    # Simplificados (R)
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0005-e000544-r.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0006-e000544-r.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/sp/sp-c0007-e000544-r.json",
    
    # Official (U)
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0005-e000544-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0005-e000544-r.json",
    
    # Check if there is another directory structure
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0005-e000544-u.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0005-e000544-r.json",
]

for url in urls:
    try:
        r = requests.head(url, timeout=5)
        print(f"URL: {url} -> Status: {r.status_code}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
