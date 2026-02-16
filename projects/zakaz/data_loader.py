import pandas as pd
import re
from typing import Optional
from address_processor import normalize_address_series


def load_installations_data(file_path: str, date_column: Optional[str] = None,
                           usecols: Optional[list] = None) -> pd.DataFrame:
    kwargs = {'engine': 'openpyxl'}
    if usecols:
        kwargs['usecols'] = usecols
    df = pd.read_excel(file_path, **kwargs)
    print(f"Загружено строк: {len(df)}")
    return df


def preprocess_data(df: pd.DataFrame, address_column: str, date_column: str,
                    sc_column: Optional[str] = None, city_column: Optional[str] = None) -> pd.DataFrame:
    processed_df = df.copy()
    if address_column not in processed_df.columns:
        raise ValueError(f"Колонка '{address_column}' не найдена в данных")
    processed_df['address_normalized'] = normalize_address_series(processed_df[address_column])

    if date_column not in processed_df.columns:
        raise ValueError(f"Колонка '{date_column}' не найдена в данных")
    processed_df['date'] = pd.to_datetime(processed_df[date_column], format='%d.%m.%Y %H:%M:%S', errors='coerce')
    if processed_df['date'].isna().any():
        processed_df['date'] = pd.to_datetime(processed_df[date_column], errors='coerce')
    processed_df = processed_df.dropna(subset=['date'])

    processed_df['year'] = processed_df['date'].dt.year
    processed_df['month'] = processed_df['date'].dt.month
    processed_df['week'] = processed_df['date'].dt.isocalendar().week
    processed_df['year_week'] = processed_df['date'].dt.strftime('%Y-W%U')

    if sc_column and sc_column in processed_df.columns:
        processed_df['sc'] = processed_df[sc_column]
    else:
        for name in ['СЦ', 'sc', 'SC', 'сервисный центр', 'сервисный_центр']:
            if name in processed_df.columns:
                processed_df['sc'] = processed_df[name]
                break
        else:
            processed_df['sc'] = 'Не указано'

    if city_column and city_column in processed_df.columns:
        if city_column == 'Территория':
            processed_df['city'] = extract_city_from_territory_series(processed_df[city_column])
        else:
            processed_df['city'] = processed_df[city_column]
    else:
        for name in ['Город', 'город', 'city', 'City', 'населенный пункт', 'населенный_пункт', 'Территория']:
            if name in processed_df.columns:
                if name == 'Территория':
                    processed_df['city'] = extract_city_from_territory_series(processed_df[name])
                else:
                    processed_df['city'] = processed_df[name]
                break
        else:
            processed_df['city'] = extract_city_from_address_series(processed_df['address_normalized'])

    processed_df['city_from_address'] = extract_city_from_address_series(processed_df['address_normalized'])
    addr_city = processed_df['city_from_address']
    use_from_addr = (addr_city.notna()) & (addr_city != 'Не указано') & (addr_city.str.len() > 0)
    processed_df.loc[use_from_addr, 'city'] = processed_df.loc[use_from_addr, 'city_from_address']
    return processed_df


def extract_city_from_territory_series(series):
    s = series.astype(str)
    city = s.str.extract(r'г\.\s*([А-Яа-яЁёA-Za-z]+)', flags=re.IGNORECASE)[0]
    fallback = s.str.replace(r'^(ПФ|ГЦТЭТ|ЛТЦ)\s*', '', flags=re.IGNORECASE, regex=True).str.strip()
    fallback = fallback.str.split().str.get(0)
    city = city.fillna(fallback).fillna("Не указано")
    return city.where(city.str.len() > 2, "Не указано")


def extract_city_from_address_series(series):
    s = series.astype(str)
    stop_pattern = r'(?=\s+ул\.|\s+пер\.|\s+пл\.|\s+пр-кт\.|\s+пр\.|\s+д\.|\s+мкр\.|\s+с\.|\s+снт\.|\s+тер\.|,|$)'
    city = s.str.extract(r'г\.\s*([^,]+?)' + stop_pattern, flags=re.IGNORECASE)[0]
    city = city.str.replace(r'^(город|г\.?)\s*', '', case=False, regex=True).str.strip()
    selo = s.str.extract(r'с\.\s*([^,]+?)' + stop_pattern, flags=re.IGNORECASE)[0]
    selo = selo.str.strip()
    city = city.fillna(selo)
    other = s.str.extract(r'^([^,]+?)(?:\s*,|\s+ул\.|\s+пер\.)', flags=re.IGNORECASE)[0]
    other = other.str.replace(r'^(город|г\.?)\s*', '', case=False, regex=True).str.strip()
    has_selo = other.str.contains(r'\s+с\.\s+', na=False, regex=True)
    selo_part = other.str.extract(r'\s+с\.\s+(\S+)', expand=False)
    other = other.where(~has_selo, 'с. ' + selo_part)
    city = city.fillna(other).fillna("Не указано")
    return city.where(city.str.len() > 0, "Не указано")
