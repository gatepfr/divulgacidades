import requests

url = "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json"
try:
    r = requests.get(url, timeout=5)
    print(f"BR URL status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("Keys:", list(data.keys()))
except Exception as e:
    print(f"Error: {e}")
