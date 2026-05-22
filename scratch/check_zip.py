import requests

url = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip"
try:
    r = requests.head(url, timeout=10)
    print("Status Code:", r.status_code)
    print("Headers:")
    for k, v in r.headers.items():
        print(f"  {k}: {v}")
except Exception as e:
    print("Error:", e)
