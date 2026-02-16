import pandas as pd
import numpy as np
from typing import Dict
from math import radians, cos, sin, asin, sqrt


def create_areas(df: pd.DataFrame, 
                 lat_col: str = 'Широта',
                 lon_col: str = 'Долгота',
                 address_col: str = 'address_normalized',
                 city_col: str = 'city',
                 max_houses_per_area: int = 15,
                 max_travel_time_minutes: float = 15.0,
                 avg_speed_kmh: float = 30.0) -> pd.DataFrame:
    df_result = df.copy()
    df_result['area'] = ''
    
    if lat_col not in df_result.columns or lon_col not in df_result.columns:
        print("ПРЕДУПРЕЖДЕНИЕ: Колонки с координатами не найдены. Области не будут созданы.")
        return df_result
    max_distance_km = (max_travel_time_minutes / 60.0) * avg_speed_kmh
    unique_addrs = df_result.groupby(address_col).agg({
        lat_col: 'first',
        lon_col: 'first',
        city_col: 'first'
    }).reset_index()
    
    unique_addrs = unique_addrs.dropna(subset=[lat_col, lon_col])
    if len(unique_addrs) == 0:
        print("ПРЕДУПРЕЖДЕНИЕ: Нет данных с координатами. Области не будут созданы.")
        return df_result
    print(f"  Уникальных адресов с координатами: {len(unique_addrs)}")
    all_area_labels = {}
    unique_cities = unique_addrs[city_col].unique()
    total_areas = 0
    
    for city in unique_cities:
        city_addrs = unique_addrs[unique_addrs[city_col] == city].copy()
        
        if len(city_addrs) == 0:
            continue
        area_map_raw = _grid_cluster(
            city_addrs, 
            address_col=address_col,
            lat_col=lat_col, 
            lon_col=lon_col,
            max_distance_km=max_distance_km,
            max_houses_per_area=max_houses_per_area
        )
        city_prefix = _safe_area_prefix(str(city))
        area_map = {addr: f"{city_prefix}-{label}" for addr, label in area_map_raw.items()}
        
        num_areas = len(set(area_map.values()))
        total_areas += num_areas
        all_area_labels.update(area_map)
        print(f"  Город {city}: {len(city_addrs)} адресов → {num_areas} областей")
    df_result['area'] = df_result[address_col].map(all_area_labels).fillna('')
    
    print(f"\nВсего создано областей: {total_areas}")
    return df_result


def _grid_cluster(df: pd.DataFrame, address_col: str, lat_col: str, lon_col: str,
                  max_distance_km: float, max_houses_per_area: int) -> Dict[str, str]:
    addresses = df[address_col].values
    lats = df[lat_col].values.astype(float)
    lons = df[lon_col].values.astype(float)
    
    coord_map = {}
    for i in range(len(addresses)):
        coord_map[addresses[i]] = (lats[i], lons[i])
    cell_size_km = max_distance_km / sqrt(2.0)
    avg_lat = float(np.mean(lats))
    lat_step = cell_size_km / 111.0
    lon_step = cell_size_km / (111.0 * cos(radians(avg_lat)))
    cells = {}
    
    for addr, (lat, lon) in coord_map.items():
        cell_row = int(lat / lat_step)
        cell_col = int(lon / lon_step)
        cell_key = (cell_row, cell_col)
        
        if cell_key not in cells:
            cells[cell_key] = []
        cells[cell_key].append(addr)
    final_cells = {}
    for cell_key, cell_addrs in cells.items():
        if len(cell_addrs) <= max_houses_per_area:
            final_cells[cell_key] = cell_addrs
        else:
            subcells = _subdivide_cell(
                cell_addrs, coord_map,
                cell_key, lat_step, lon_step, max_houses_per_area
            )
            for sub_key, sub_addrs in subcells.items():
                final_cells[sub_key] = sub_addrs
    area_map = {}
    sorted_cells = sorted(final_cells.keys())
    
    for area_idx, cell_key in enumerate(sorted_cells):
        label = _area_label(area_idx)
        for addr in final_cells[cell_key]:
            area_map[addr] = label
    
    return area_map


def _subdivide_cell(cell_addrs, coord_map, cell_key, lat_step, lon_step, max_houses_per_area):
    half_lat = lat_step / 2.0
    half_lon = lon_step / 2.0
    
    subcells = {}
    for addr in cell_addrs:
        lat, lon = coord_map[addr]
        sub_row = int(lat / half_lat)
        sub_col = int(lon / half_lon)
        sub_key = (cell_key[0], cell_key[1], sub_row, sub_col)
        
        if sub_key not in subcells:
            subcells[sub_key] = []
        subcells[sub_key].append(addr)
    result = {}
    for sub_key, addrs in subcells.items():
        if len(addrs) <= max_houses_per_area:
            result[sub_key] = addrs
        else:
            for i in range(0, len(addrs), max_houses_per_area):
                chunk = addrs[i:i + max_houses_per_area]
                chunk_key = (*sub_key, i)
                result[chunk_key] = chunk
    
    return result


def _safe_area_prefix(city_name: str) -> str:
    s = city_name.strip()
    for c in ' .,;:\t':
        s = s.replace(c, '_')
    return s[:30] if s else 'Город'


def _area_label(index: int) -> str:
    if index < 26:
        return ' ' + chr(ord('A') + index)
    index -= 26
    return chr(ord('A') + index // 26) + chr(ord('A') + index % 26)
