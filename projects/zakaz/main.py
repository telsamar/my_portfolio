import numpy as np
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
from data_loader import load_installations_data, preprocess_data
from forecast_model import InstallationForecastModel
from config_manager import ForecastConfig, create_default_config
from area_clustering import create_areas

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
INPUT_FILENAME = 'my_file_result.xlsx'
OUTPUT_FILENAME = 'forecast_result.xlsx'
ADDRESS_COLUMN = 'Адрес до квартиры'
DATE_COLUMN = 'Последняя назначенная дата'
SC_COLUMN = 'СЦ'
CITY_COLUMN = 'Территория'
LAT_COLUMN = 'Широта'
LON_COLUMN = 'Долгота'
MAX_HOUSES_PER_AREA = 15
MAX_TRAVEL_TIME_MINUTES = 15.0
AVG_SPEED_KMH = 30.0
CONFIG_FILE = os.path.join(INPUT_DIR, 'forecast_config.json')


def generate_forecast(input_file: str, output_file: str, address_column: str, date_column: str,
                     sc_column: str = None, city_column: str = None):
    print("=" * 60)
    print("Модель прогнозирования заявок на инсталляции")
    print("=" * 60)
    print("\n[1/5] Загрузка данных...")
    try:
        df = load_installations_data(input_file)
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        sys.exit(1)
    if address_column not in df.columns:
        print(f"ОШИБКА: Колонка '{address_column}' не найдена в данных")
        print("Доступные колонки:", df.columns.tolist())
        sys.exit(1)
    
    if date_column not in df.columns:
        print(f"ОШИБКА: Колонка '{date_column}' не найдена в данных")
        print("Доступные колонки:", df.columns.tolist())
        sys.exit(1)
    
    print(f"Используется колонка с адресом: {address_column}")
    print(f"Используется колонка с датой: {date_column}")
    
    has_coords = LAT_COLUMN in df.columns and LON_COLUMN in df.columns
    if has_coords:
        print(f"Найдены координаты: {LAT_COLUMN}, {LON_COLUMN}")
    else:
        print("Координаты не найдены — области не будут созданы")
    
    if sc_column and sc_column not in df.columns:
        print(f"ПРЕДУПРЕЖДЕНИЕ: Колонка '{sc_column}' не найдена, будет использовано значение по умолчанию")
        sc_column = None
    
    if city_column and city_column not in df.columns:
        print(f"ПРЕДУПРЕЖДЕНИЕ: Колонка '{city_column}' не найдена, город будет извлечен из адреса")
        city_column = None
    print("\n[2/5] Предобработка данных...")
    try:
        df_processed = preprocess_data(
            df, 
            address_column=address_column,
            date_column=date_column,
            sc_column=sc_column,
            city_column=city_column
        )
        print(f"Обработано строк: {len(df_processed)}")
        print(f"Уникальных адресов: {df_processed['address_normalized'].nunique()}")
    except Exception as e:
        print(f"Ошибка при предобработке данных: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    print("\n[3/5] Применение конфигурации исключений и коэффициентов...")
    config = ForecastConfig(CONFIG_FILE)
    df_processed = config.apply_to_dataframe(df_processed, city_column='city', date_column='date')
    print("\n[4/5] Создание областей...")
    if has_coords and LAT_COLUMN in df_processed.columns and LON_COLUMN in df_processed.columns:
        df_processed = create_areas(
            df_processed,
            lat_col=LAT_COLUMN,
            lon_col=LON_COLUMN,
            address_col='address_normalized',
            city_col='city',
            max_houses_per_area=MAX_HOUSES_PER_AREA,
            max_travel_time_minutes=MAX_TRAVEL_TIME_MINUTES,
            avg_speed_kmh=AVG_SPEED_KMH
        )
    else:
        print("Пропуск — координаты отсутствуют")
        df_processed['area'] = ''
    print("\n[5/5] Анализ данных и генерация прогноза...")
    model = InstallationForecastModel()
    model.fit(df_processed, weight_col='weight')
    print(f"Проанализировано данных для {len(model.historical_stats)} адресов")
    group_cols = ['sc', 'city', 'address_normalized']
    if 'area' in df_processed.columns:
        group_cols = ['area'] + group_cols
    
    df_for_locations = df_processed[df_processed['weight'] > 0] if 'weight' in df_processed.columns else df_processed
    unique_locations = df_for_locations.groupby(group_cols).size().reset_index()
    unique_locations = unique_locations[group_cols]
    if 'city_from_address' in df_processed.columns:
        addr_to_city = df_processed.drop_duplicates('address_normalized')[['address_normalized', 'city_from_address']].set_index('address_normalized')['city_from_address']
        display_city = unique_locations['address_normalized'].map(addr_to_city)
        mask_use = (display_city.notna()) & (display_city != 'Не указано') & (display_city.str.len() > 0)
        unique_locations['city_display'] = unique_locations['city'].where(~mask_use, display_city)
    else:
        unique_locations['city_display'] = unique_locations['city']
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    forecast_daily_date = today + timedelta(days=1)

    forecast_start_date = today
    days_until_monday = (7 - forecast_start_date.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    forecast_start_date = forecast_start_date + timedelta(days=days_until_monday)

    addresses = unique_locations['address_normalized'].values
    next_month = forecast_start_date.replace(day=1) + timedelta(days=32)
    month_start = next_month.replace(day=1)
    daily_arr = model.predict_daily_batch(addresses, forecast_daily_date)
    weekly_arr = model.predict_weekly_batch(addresses, forecast_start_date)
    monthly_arr = model.predict_monthly_batch(addresses, month_start)
    raw_area = unique_locations['area'].fillna('') if 'area' in unique_locations.columns else pd.Series([''] * len(unique_locations))
    area_suffix = raw_area.str.split('-', n=1).str[-1].str.strip().replace('', np.nan)
    city_display_ser = unique_locations['city_display'] if 'city_display' in unique_locations.columns else unique_locations['city']
    area_vals = np.where(area_suffix.notna(), city_display_ser + '-' + area_suffix, raw_area.values)
    city_display = unique_locations['city_display'].values if 'city_display' in unique_locations.columns else unique_locations['city'].values
    forecast_df = pd.DataFrame({
        'Область': area_vals,
        'СЦ': unique_locations['sc'].values,
        'Населенный пункт': city_display,
        'Адрес до дома': addresses,
        'Прогноз заявок на день': np.round(daily_arr, 1),
        'Прогноз заявок на неделю': np.round(weekly_arr, 1),
        'Прогноз заявок на месяц': np.round(monthly_arr, 1)
    })
    def _area_sort_key(val):
        if pd.isna(val) or val == '':
            return ('', 0, '')
        parts = str(val).rsplit('-', 1)
        if len(parts) < 2:
            return (str(val), 0, '')
        city_part, suffix = parts[0].strip(), parts[1].strip()
        return (city_part, len(suffix), suffix)
    forecast_df['_area_order'] = forecast_df['Область'].apply(_area_sort_key)
    forecast_df = forecast_df.sort_values(
        ['_area_order', 'СЦ', 'Населенный пункт', 'Адрес до дома']
    ).drop(columns=['_area_order'])
    print(f"\nСохранение результатов в {output_file}...")
    forecast_df.to_excel(output_file, index=False, engine='openpyxl')
    
    print("\n" + "=" * 60)
    print("Прогноз успешно сгенерирован!")
    print("=" * 60)
    print(f"\nВсего адресов в прогнозе: {len(forecast_df)}")
    print(f"\nПервые 10 строк прогноза:")
    print(forecast_df.head(10).to_string(index=False))
    print(f"\n\nРезультаты сохранены в файл: {output_file}")


if __name__ == "__main__":
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    input_file_path = os.path.join(INPUT_DIR, INPUT_FILENAME)
    output_file_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    if not os.path.exists(input_file_path):
        print(f"ОШИБКА: Входной файл '{input_file_path}' не найден!")
        print(f"Поместите файл с данными в папку '{INPUT_DIR}/' с именем '{INPUT_FILENAME}'")
        print(f"Текущая директория: {os.getcwd()}")
        sys.exit(1)
    if not os.path.exists(CONFIG_FILE):
        print(f"\nФайл конфигурации {CONFIG_FILE} не найден. Создание по умолчанию...")
        create_default_config(CONFIG_FILE)
        print()
    print(f"Входной файл: {input_file_path}")
    print(f"Выходной файл: {output_file_path}")
    print(f"Файл конфигурации: {CONFIG_FILE}")
    print()
    
    generate_forecast(
        input_file=input_file_path,
        output_file=output_file_path,
        address_column=ADDRESS_COLUMN,
        date_column=DATE_COLUMN,
        sc_column=SC_COLUMN,
        city_column=CITY_COLUMN
    )
