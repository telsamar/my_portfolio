import json
import os
from datetime import datetime


class ForecastConfig:
    def __init__(self, config_file: str = 'input/forecast_config.json'):
        self.config_file = config_file
        self.exclusions = []
        self.coefficients = []
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.exclusions = config.get('exclusions', [])
                    self.coefficients = config.get('coefficients', [])
                print(f"Загружена конфигурация из {self.config_file}")
                print(f"  Исключений: {len(self.exclusions)}")
                print(f"  Коэффициентов: {len(self.coefficients)}")
            except Exception as e:
                print(f"Ошибка при загрузке конфигурации: {e}")
                print("Используются настройки по умолчанию")
        else:
            print(f"Файл конфигурации {self.config_file} не найден, используются настройки по умолчанию")

    def should_exclude(self, city: str, date: datetime) -> bool:
        for exclusion in self.exclusions:
            if exclusion.get('city', '').lower() not in city.lower():
                continue
            if 'month' in exclusion and date.month != exclusion['month']:
                continue
            if 'year' in exclusion and date.year != exclusion['year']:
                continue
            return True
        return False

    def get_coefficient(self, city: str, date: datetime) -> float:
        for coeff_config in self.coefficients:
            if coeff_config.get('city', '').lower() not in city.lower():
                continue
            if 'month' in coeff_config and date.month != coeff_config['month']:
                continue
            if 'year' in coeff_config and date.year != coeff_config['year']:
                continue
            return coeff_config.get('coefficient', 1.0)
        return 1.0

    def apply_to_dataframe(self, df, city_column: str = 'city', date_column: str = 'date'):
        import numpy as np
        df_processed = df.copy()
        n = len(df_processed)
        weight = np.ones(n, dtype=float)
        cities = df_processed[city_column].astype(str).str.lower()
        dates = df_processed[date_column]
        months = dates.dt.month.values
        years = dates.dt.year.values

        excluded_count = 0
        weighted_count = 0

        for exclusion in self.exclusions:
            city_match = exclusion.get('city', '').lower()
            if not city_match:
                continue
            mask = cities.str.contains(city_match, regex=False)
            if 'month' in exclusion:
                mask = mask & (months == exclusion['month'])
            if 'year' in exclusion:
                mask = mask & (years == exclusion['year'])
            cnt = mask.sum()
            if cnt > 0:
                weight[mask.values] = 0.0
                excluded_count += int(cnt)

        for coeff_config in self.coefficients:
            city_match = coeff_config.get('city', '').lower()
            if not city_match:
                continue
            coeff = coeff_config.get('coefficient', 1.0)
            if coeff == 1.0:
                continue
            mask = cities.str.contains(city_match, regex=False) & (weight > 0)
            if 'month' in coeff_config:
                mask = mask & (months == coeff_config['month'])
            if 'year' in coeff_config:
                mask = mask & (years == coeff_config['year'])
            cnt = mask.sum()
            if cnt > 0:
                weight[mask.values] = coeff
                weighted_count += int(cnt)

        df_processed['weight'] = weight
        if excluded_count > 0:
            print(f"  Исключено записей: {excluded_count}")
        if weighted_count > 0:
            print(f"  Применены коэффициенты к записям: {weighted_count}")
        return df_processed


def create_default_config(config_file: str = 'input/forecast_config.json'):
    default_config = {
        "exclusions": [],
        "coefficients": []
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=2)
    
    print(f"Создан файл конфигурации по умолчанию: {config_file}")
    print(f"Примеры правил можно найти в файле: forecast_config.example.json")
