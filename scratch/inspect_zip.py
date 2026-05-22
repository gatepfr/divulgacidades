import zipfile

zip_path = "scratch/votacao_candidato_munzona_2022.zip"

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        print("Total files in ZIP:", len(file_list))
        print("First 10 files:")
        for name in file_list[:10]:
            print(f"  {name}")
            
        # Find one CSV file to inspect
        csv_files = [f for f in file_list if f.endswith('.csv') or f.endswith('.txt')]
        if csv_files:
            target_file = csv_files[0]
            print(f"\nInspecting the first 5 lines of {target_file}:")
            with zip_ref.open(target_file) as f:
                for i in range(5):
                    line = f.readline().decode('latin1') # TSE usually uses ISO-8859-1 / latin1
                    print(line.strip())
        else:
            print("No CSV/TXT files found in ZIP.")
except Exception as e:
    print("Error:", e)
