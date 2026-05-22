import requests

url = "https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0005-e000544-u.json"
try:
    response = requests.get(url, timeout=10)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Success! State-wide Senator data exists.")
        print(response.json().keys())
except Exception as e:
    print("Error:", e)
