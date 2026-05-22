import requests

# Let's test the 2022 photo URL with candidate Garibalde from Sergipe
# sq_candidato: 260001669431, uf: se (lowercase), pleito: 546
url = "https://resultados.tse.jus.br/oficial/ele2022/546/fotos/se/260001669431.jpeg"

try:
    r = requests.head(url, timeout=10)
    print("URL:", url)
    print("Status:", r.status_code)
    
    # Try uppercase SE
    url2 = "https://resultados.tse.jus.br/oficial/ele2022/546/fotos/SE/260001669431.jpeg"
    r2 = requests.head(url2, timeout=10)
    print("URL2:", url2)
    print("Status2:", r2.status_code)
    
    # Try pleito 544
    url3 = "https://resultados.tse.jus.br/oficial/ele2022/544/fotos/se/260001669431.jpeg"
    r3 = requests.head(url3, timeout=10)
    print("URL3:", url3)
    print("Status3:", r3.status_code)
    
except Exception as e:
    print("Error:", e)
