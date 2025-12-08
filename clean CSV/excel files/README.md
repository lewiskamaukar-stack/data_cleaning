# Data Cleaning Automation

This project is a Python-based CSV cleaning automation tool. It handles messy CSV files and produces **cleaned, standardized CSVs**.

## Features
- Adds `product_id` automatically
- Cleans `product_name` and `category` (title case, removes extra spaces)
- Converts `price` and `stock` to numeric
- Standardizes `launch_date` to `YYYY-MM-DD`
- Optional **category filter**
- Optional **price alerts** (above or below threshold)
- Batch processing of multiple CSVs

## Usage

### Basic Cleaning
```bash
python clean_data.py raw_csvs cleaned_csvs
