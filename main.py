import pandas as pd

# Завантаження даних з локального CSV-файлу з вказаним кодуванням
file_path = 'investments_VC.csv'

# Спробуйте різні кодування, якщо це не спрацює
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

# Порівняння середнього фінансування компаній зі США та інших країн
us_companies = df[df['country_code'] == 'USA']
other_companies = df[df['country_code'] != 'USA']

mean_funding_us = us_companies['funding_total_usd'].mean()
mean_funding_other = other_companies['funding_total_usd'].mean()

print(f"Середнє фінансування компаній зі США: ${mean_funding_us:,.2f}")
print(f"Середнє фінансування компаній з інших країн: ${mean_funding_other:,.2f}")

# Перевірка гіпотези
if mean_funding_us > mean_funding_other:
    print("Гіпотеза підтверджена: компанії зі США отримують значно більше фінансування ніж компанії з інших країн.")
else:
    print("Гіпотеза не підтверджена.")