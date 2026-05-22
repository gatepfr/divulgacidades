import requests
import os
import sys

url = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip"
dest = "scratch/votacao_candidato_munzona_2022.zip"

os.makedirs("scratch", exist_ok=True)

print(f"Downloading {url} to {dest}...")
try:
    # Use streaming to download
    response = requests.get(url, stream=True, timeout=30)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024 # 1 MB chunks
    
    downloaded = 0
    with open(dest, "wb") as f:
        for data in response.iter_content(block_size):
            f.write(data)
            downloaded += len(data)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"Downloaded: {downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB ({percent:.1f}%)", end="\r")
            else:
                print(f"Downloaded: {downloaded / 1024 / 1024:.2f} MB", end="\r")
            sys.stdout.flush()
    print("\nDownload completed successfully!")
except Exception as e:
    print(f"\nError occurred: {e}")
