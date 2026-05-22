import requests

url = "https://resultados.tse.jus.br/oficial/ele2024/619/fotos/sp/250002098117.jpeg"
try:
    r = requests.head(url, timeout=10)
    print("URL:", url)
    print("Status:", r.status_code)
    print("Headers:", dict(r.headers))
except Exception as e:
    print("Error:", e)
