import requests

def test_url(url):
    try:
        response = requests.get(url, timeout=10)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Keys:", list(data.keys())[:5])
            if 'candidatos' in data:
                print("Num Candidates:", len(data['candidatos']))
            elif 'agr' in data:
                # 2024 format might have different structure
                print("Top-level keys sample:", list(data.keys()))
            return True
    except Exception as e:
        print(f"Error for {url}: {e}")
    return False

print("--- TESTING 2024 MUNICIPAL (SP - São Paulo: 71072) ---")
# Prefeito 2024
test_url("https://resultados.tse.jus.br/oficial/ele2024/619/dados/sp/sp71072-c0011-e000619-u.json")
# Vereador 2024
test_url("https://resultados.tse.jus.br/oficial/ele2024/619/dados/sp/sp71072-c0013-e000619-u.json")

print("\n--- TESTING 2022 MUNICIPAL (SP - São Paulo: 71072) ---")
# Senador 2022
test_url("https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0005-e000544-u.json")
# Deputado Federal 2022
test_url("https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0006-e000544-u.json")
# Deputado Estadual 2022
test_url("https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp71072-c0007-e000544-u.json")

print("\n--- TESTING 2022 STATE-WIDE ---")
# Senador 2022 State-wide
test_url("https://resultados.tse.jus.br/oficial/ele2022/544/dados/sp/sp-c0005-e000544-u.json")
