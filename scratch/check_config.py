import requests

urls = [
    "https://resultados.tse.jus.br/oficial/ele2022/546/config/mun-e000546-cm.json",
    "https://resultados.tse.jus.br/oficial/ele2022/546/config/ele-c.json",
    "https://resultados.tse.jus.br/oficial/ele2022/544/config/ele-c.json",
]

for url in urls:
    r = requests.get(url)
    print(f"URL: {url} -> Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Content length: {len(r.text)}")
        try:
            data = r.json()
            print("Keys:", list(data.keys())[:10])
            # If it's ele-c.json, print some info
            if 'e' in data:
                print("Elections:", [e.get('cd') for e in data.get('e', [])])
        except:
            print("Not JSON or failed to parse")
