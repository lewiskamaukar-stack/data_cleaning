#!/usr/bin/env python3
"""
clean_data.py

Usage:
    python clean_data.py input.csv output_clean.csv
    or
    python clean_data.py --input-folder ./raw_csvs --output-folder ./cleaned
"""

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import re

def clean_dataframe(df):
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]

    obj_cols = df.select_dtypes(include=['object']).columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({'': np.nan, 'nan': np.nan, 'N/A': np.nan, 'n/a': np.nan})

    if 'product_name' in df.columns:
        df['product_name'] = df['product_name'].str.title()

    if 'category' in df.columns:
        df['category'] = df['category'].str.title()

    if 'product_id' in df.columns:
        df['product_id'] = df['product_id'].astype(str).str.strip().str.zfill(3)

    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).replace(r'(^nan$)|(^None$)', np.nan, regex=True)
        df['price'] = df['price'].str.replace(r'[^0-9\.\-]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').round(2)

    if 'stock' in df.columns:
        df['stock'] = df['stock'].astype(str).str.replace(r'[^0-9\-]', '', regex=True)
        df['stock'] = pd.to_numeric(df['stock'], errors='coerce').fillna(0).astype(int)

    if 'launch_date' in df.columns:
        df['launch_date'] = pd.to_datetime(df['launch_date'], errors='coerce').dt.date


    preferred = ['product_id', 'product_name', 'category', 'price', 'stock', 'launch_date']
    existing = [c for c in preferred if c in df.columns]
    others = [c for c in df.columns if c not in existing]
    df = df[existing + others]

    return df

def clean_file(input_path, output_csv=None, output_xlsx=None):
    df = pd.read_csv(input_path, dtype= str)
    cleaned = clean_dataframe(df)
    if output_csv:
        cleaned.to_csv(output_csv, index=False)
    if output_xlsx:
        cleaned.to_excel(output_xlsx, index=False)
    return cleaned

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', dest='input', help='Input CSV file path')
    p.add_argument('--output', '-o', dest='output', default=None, help='Output CSV file path')
    p.add_argument('--excel', dest='excel', default=None, help='Output Excel file path')
    p.add_argument('--input-folder', dest='input_folder', default=None)
    p.add_argument('--output-folder', dest='output_folder', default=None)
    args = p.parse_args()

    if args.input:
        inp = Path(args.input)
        out_csv = args.output or str(inp.with_name(inp.stem + '_cleaned.csv'))
        out_xlsx = args.excel or str(inp.with_name(inp.stem + '_cleaned.xlsx'))
        cleaned = clean_file(inp, out_csv, out_xlsx)
        print(f"Saved cleaned files:\n - {out_csv}\n - {out_xlsx}")
        print(cleaned.head())
    elif args.input_folder:
        inp_folder = Path(args.input_folder)
        out_folder = Path(args.output_folder or inp_folder / 'cleaned')
        out_folder.mkdir(parents=True, exist_ok=True)
        for f in inp_folder.glob('*.csv'):
            out_csv = out_folder / f.name.replace('.csv', '_cleaned.csv')
            out_xlsx = out_folder / f.name.replace('.csv', '_cleaned.xlsx')
            clean_file(f, out_csv, out_xlsx)
            print("Processed:", f.name)
        print("Done. Cleaned files in:", out_folder)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
