import re


def normalize_address_series(series):
    out = series.astype(str).str.strip()
    for p in [r',\s*кв\.?\s*\d+[-\d]*', r',\s*квартира\s*\d+[-\d]*', r',\s*к\.\s*\d+[-\d]*',
              r'\s+кв\.?\s*\d+[-\d]*', r'\s+квартира\s*\d+[-\d]*', r'\s+к\.\s*\d+[-\d]*']:
        out = out.str.replace(p, '', case=False, regex=True)
    out = out.str.replace(r',\s*,', ',', regex=True).str.replace(r',\s*$', '', regex=True)
    out = out.str.replace(r'\s+', ' ', regex=True).str.strip()
    return out
