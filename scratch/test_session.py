import json
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Create a thread-safe Session with a connection pool
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=24, pool_maxsize=24)
session.mount("https://", adapter)

with open("scratch/mapped_cities.json", "r", encoding="utf-8") as f:
    mapped_cities = json.load(f)

# Take 100 cities that are currently missing
missing_tasks = []
for uf, cities in mapped_cities.items():
    for city_name, tse_code in cities.items():
        file_name = f"{uf}_{city_name.replace(' ', '_')}.json"
        path = f"scratch/parsed_2024/{file_name}"
        if not os.path.exists(path):
            missing_tasks.append((uf, city_name, tse_code))
        if len(missing_tasks) >= 100:
            break
    if len(missing_tasks) >= 100:
        break

print(f"Testing session-based concurrency with {len(missing_tasks)} cities...")

def get_json(url):
    for i in range(3):
        try:
            r = session.get(url, timeout=5)
            return r.status_code
        except Exception as e:
            pass
    return 500

def test_city(task):
    uf, city_name, tse_code = task
    uf_lower = uf.lower()
    # Fetch Prefeito
    url_pref = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf_lower}/{uf_lower}{tse_code}-c0011-e000619-u.json"
    status_pref = get_json(url_pref)
    # Fetch Vereador
    url_ver = f"https://resultados.tse.jus.br/oficial/ele2024/619/dados/{uf_lower}/{uf_lower}{tse_code}-c0013-e000619-u.json"
    status_ver = get_json(url_ver)
    return status_pref, status_ver

start_time = time.time()
status_codes = []

with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(test_city, t): t for t in missing_tasks}
    for future in as_completed(futures):
        status_codes.append(future.result())

end_time = time.time()
duration = end_time - start_time
print(f"Completed 100 cities in {duration:.2f} seconds.")
print(f"Average speed: {100 / duration:.2f} cities/sec.")

pref_statuses = [s[0] for s in status_codes]
ver_statuses = [s[1] for s in status_codes]

print("Prefeito statuses:", {x: pref_statuses.count(x) for x in set(pref_statuses)})
print("Vereador statuses:", {x: ver_statuses.count(x) for x in set(ver_statuses)})
