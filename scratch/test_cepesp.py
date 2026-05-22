import requests

# Test CEPESP API query
url = "https://cepesp.io/api/consulta/athena/query"
params = {
    "table": "votos",
    "anos": "2022",
    "cargo": "5",       # 5 = Senador
    "uf_filter": "SP",
    "limit": "10"
}

try:
    r = requests.get(url, params=params, timeout=10)
    print("Status:", r.status_code)
    if r.status_code == 200:
        data = r.json()
        print("Data type:", type(data))
        if isinstance(data, list):
            print("Length:", len(data))
            if data:
                print("First record:", data[0])
        elif isinstance(data, dict):
            print("Keys:", list(data.keys()))
            # E.g. results might be under a key
            for k in list(data.keys()):
                val = data[k]
                print(f"Key {k} type: {type(val)}")
                if isinstance(val, list) and val:
                    print(f"Key {k} list sample:", val[0])
except Exception as e:
    print("Error:", e)
