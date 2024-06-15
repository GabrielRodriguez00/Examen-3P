import requests
import hashlib
import pandas as pd
import time
import sqlite3
from tabulate import tabulate


# Módulo de obtención de datos
def get_all_data():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    return response.json()

def get_country_data(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    return response.json()

# Módulo de procesamiento de datos
def encrypt_language(language_name):
    return hashlib.sha1(language_name.encode('utf-8')).hexdigest()

def process_country_data():
    countries = get_all_data()
    records = []
    for country in countries:
        start_time = time.monotonic()
        country_data = get_country_data(country['name']['common'])
        region = country_data[0].get('region', 'Unknown')
        city_name = country_data[0]['name']['common']
        languages = country_data[0].get('languages', {})
        for lang_code, lang_name in languages.items():
            encrypted_language = encrypt_language(lang_name)
            end_time = time.monotonic()
            pTime = end_time - start_time
            records.append({
                'Region': region,
                'País': city_name,
                'Idioma': lang_name,
                'Idioma encriptado': encrypted_language,
                'Tiempo en ms': pTime * 1000
            })
    return records

# Módulo de análisis y almacenamiento
def analyze_and_store_data(records):
    df = pd.DataFrame(records)
    print("DataFrame de registros procesados:")
    
    print(tabulate(df, headers='keys', tablefmt='psql'))

    total_time = df['Tiempo en ms'].sum()
    average_time = df['Tiempo en ms'].mean()
    min_time = df['Tiempo en ms'].min()
    max_time = df['Tiempo en ms'].max()

    # Crear un DataFrame con las estadísticas
    stats = pd.DataFrame({
        'Tiempo total': [total_time],
        'Tiempo promedio': [average_time],
        'Tiempo mínimo': [min_time],
        'Tiempo máximo': [max_time]
    })

    conn = sqlite3.connect('countries.db')
    df.to_sql('country_languages', conn, if_exists='replace', index=False)
    conn.close()

    df.to_json('data.json', orient='records')

    return stats

# Función principal
def main():
    records = process_country_data()
    analysis_df = analyze_and_store_data(records)
    print("\n DataFrame de estadísticas en ms:")
    print(tabulate(analysis_df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()