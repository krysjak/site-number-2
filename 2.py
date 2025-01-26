import pandas as pd

# Завантаження даних з локального CSV-файлу з вказаним кодуванням
file_path = 'investments_VC.csv'
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

for encoding in encodings:
    try:
        df = pd.read_csv(file_path, encoding=encoding, skipinitialspace=True)
        print(f"Файл успішно завантажено з кодуванням {encoding}")
        break
    except UnicodeDecodeError:
        print(f"Не вдалося завантажити файл з кодуванням {encoding}")

# Видалення пробілів навколо назв колонок
df.columns = df.columns.str.strip()

# Видалення пробілів у колонці 'funding_total_usd' і перетворення її в числовий формат
df['funding_total_usd'] = df['funding_total_usd'].str.replace(',', '').str.replace('"', '').str.strip()
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')

# Видалення рядків з відсутніми значеннями у колонці 'funding_total_usd'
df = df.dropna(subset=['funding_total_usd'])

# Визначення технологічного сектору
tech_sectors = ['Software', 'Internet', 'Mobile', 'Technology']

# Фільтрація компаній в технологічному секторі
tech_companies = df[df['category_list'].str.contains('|'.join(tech_sectors), na=False, case=False)]
non_tech_companies = df[~df['category_list'].str.contains('|'.join(tech_sectors), na=False, case=False)]

# Порівняння середнього фінансування
mean_funding_tech = tech_companies['funding_total_usd'].mean()
mean_funding_non_tech = non_tech_companies['funding_total_usd'].mean()

print(f"Середнє фінансування компаній в технологічному секторі: ${mean_funding_tech:,.2f}")
print(f"Середнє фінансування компаній в інших секторах: ${mean_funding_non_tech:,.2f}")

# Перевірка гіпотези
if mean_funding_tech > mean_funding_non_tech:
    print("Гіпотеза підтверджена: компанії в технологічному секторі отримують більше фінансування, ніж компанії в інших секторах.")
else:
    print("Гіпотеза не підтверджена.")