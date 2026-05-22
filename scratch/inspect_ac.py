import zipfile

zip_path = "scratch/votacao_candidato_munzona_2022.zip"
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    with zip_ref.open("votacao_candidato_munzona_2022_AC.csv") as f:
        # print first 5 lines
        for i in range(5):
            print(f.readline().decode('latin1').strip())
