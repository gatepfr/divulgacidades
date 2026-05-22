import requests

tse_code = "74136"
uf = "pr"
suffixes = ["u", "f", "r", "v", "d", "a", "s"]

print("Checking suffixes for Apucarana:")
for s in suffixes:
    url = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf}/{uf}{tse_code}-c0013-e000619-{s}.json"
    try:
        r = requests.head(url, timeout=5)
        print(f"Suffix -{s}: status {r.status_code}")
    except Exception as e:
        print(f"Suffix -{s}: error {e}")
