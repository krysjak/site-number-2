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

# Перетворення колонки 'founded_year' в числовий формат
df['founded_year'] = pd.to_numeric(df['founded_year'], errors='coerce')

# Фільтрація компаній, заснованих до і після 2010 року
companies_after_2010 = df[df['founded_year'] >= 2010]
companies_before_2010 = df[df['founded_year'] < 2010]

# Порівняння середнього фінансування
mean_funding_after_2010 = companies_after_2010['funding_total_usd'].mean()
mean_funding_before_2010 = companies_before_2010['funding_total_usd'].mean()

print(f"Середнє фінансування компаній, заснованих після 2010 року: ${mean_funding_after_2010:,.2f}")
print(f"Середнє фінансування компаній, заснованих до 2010 року: ${mean_funding_before_2010:,.2f}")

# Перевірка гіпотези
if mean_funding_after_2010 > mean_funding_before_2010:
    print("Гіпотеза підтверджена: компанії, засновані після 2010 року, отримують більше фінансування, ніж компанії, засновані до 2010 року.")
else:
    print("Гіпотеза не підтверджена.")