import pandas as pd
from datetime import datetime


class InstallationForecastModel:
    def __init__(self):
        self.historical_stats = {}

    def fit(self, df: pd.DataFrame, address_col: str = 'address_normalized', weight_col: str = 'weight'):
        df_weighted = df.copy()
        if weight_col in df_weighted.columns:
            initial_count = len(df_weighted)
            df_weighted = df_weighted[df_weighted[weight_col] > 0].copy()
            excluded = initial_count - len(df_weighted)
            if excluded > 0:
                print(f"  Исключено записей из анализа: {excluded}")
        if weight_col in df_weighted.columns:
            df_weighted['weighted_count'] = df_weighted[weight_col]
            df_grouped = df_weighted.groupby([address_col, 'date'])['weighted_count'].sum().reset_index(name='count')
        else:
            df_grouped = df_weighted.groupby([address_col, 'date']).size().reset_index(name='count')
        
        df_grouped = df_grouped.sort_values('date')
        for address, grp in df_grouped.groupby(address_col, sort=False):
            address_data = grp.set_index('date')[['count']]
            if address_data.empty:
                continue
            start, end = address_data.index.min(), address_data.index.max()
            address_data = address_data.reindex(
                pd.date_range(start=start, end=end, freq='D'),
                fill_value=0.0
            ).fillna(0)
            count_series = address_data['count'] if 'count' in address_data.columns else address_data.squeeze()
            self.historical_stats[address] = {
                'mean_daily': float(count_series.mean()),
                'mean_weekly': float(count_series.resample('W').sum().mean()),
                'mean_monthly': float(count_series.resample('ME').sum().mean()),
                'std_daily': float(count_series.std()) if len(count_series) > 1 else 0.0,
                'last_date': end,
                'total_count': float(count_series.sum()),
                'data_points': int((count_series > 0).sum())
            }

    def predict_daily_batch(self, addresses, target_date: datetime):
        import numpy as np
        out = np.zeros(len(addresses), dtype=float)
        day_adj = 1.1 if target_date.weekday() == 0 else (0.7 if target_date.weekday() in (5, 6) else 1.0)
        month_adj = 0.95 if target_date.month in (12, 1, 2) else (1.05 if target_date.month in (6, 7, 8) else 1.0)
        for i, addr in enumerate(addresses):
            if addr in self.historical_stats:
                out[i] = max(0, self.historical_stats[addr]['mean_daily'] * day_adj * month_adj)
        return out

    def predict_weekly_batch(self, addresses, start_date: datetime):
        import numpy as np
        out = np.zeros(len(addresses), dtype=float)
        adj = 0.9 if start_date.weekday() in (5, 6) else 1.0
        for i, addr in enumerate(addresses):
            if addr in self.historical_stats:
                out[i] = max(0, self.historical_stats[addr]['mean_weekly'] * adj)
        return out

    def predict_monthly_batch(self, addresses, start_date: datetime):
        import numpy as np
        out = np.zeros(len(addresses), dtype=float)
        adj = 0.95 if start_date.month in (12, 1, 2) else (1.05 if start_date.month in (6, 7, 8) else 1.0)
        for i, addr in enumerate(addresses):
            if addr in self.historical_stats:
                out[i] = max(0, self.historical_stats[addr]['mean_monthly'] * adj)
        return out
