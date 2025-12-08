import pandas as pd
import os
import sys

def clean_data(df):
    if 'product_id' not in df.columns:
        df.insert(0, "product_id", range(1, len(df) + 1))

    df['product_name'] = df['product_name'].astype(str).str.strip().str.title()
    df['category'] = df['category'].astype(str).str.strip().str.title()

    df['price'] = df['price'].astype(str).str.replace(r'[^0-9.]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    df['stock'] = pd.to_numeric(df['stock'], errors='coerce')

    df['launch_date'] = pd.to_datetime(df['launch_date'], errors='coerce').dt.strftime('%Y-%m-%d')

    return df

def load_csv(file_path):
    return pd.read_csv(file_path)

def save_csv(df, output_file):
    df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

def filter_by_category(df, category_name):
    category_name = category_name.strip().title()
    return df[df['category'] == category_name]

def price_alert(df, threshold, above=True):
    if above:
        alert_df = df[df['price'] > threshold]
    else:
        alert_df = df[df['price'] < threshold]
    if not alert_df.empty:
        print("⚠️ Price Alert! Products meeting criteria:")
        print(alert_df[['product_name', 'price']])
    return alert_df

def process_file(file_path, output_folder, category=None, price_threshold=None, above=True):
    df = load_csv(file_path)
    df = clean_data(df)

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    save_csv(df, os.path.join(output_folder, f"{base_name}_cleaned.csv"))

    if category:
        filtered_df = filter_by_category(df, category)
        save_csv(filtered_df, os.path.join(output_folder, f"{base_name}_{category}_filtered.csv"))

    if price_threshold is not None:
        price_alert(df, price_threshold, above=above)

def batch_process(input_folder, output_folder, category=None, price_threshold=None, above=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            process_file(
                os.path.join(input_folder, file),
                output_folder,
                category=category,
                price_threshold=price_threshold,
                above=above
            )

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_data.py <input_folder> <output_folder> [category] [price_threshold] [above=True/False]")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    category = sys.argv[3] if len(sys.argv) > 3 else None
    price_threshold = float(sys.argv[4]) if len(sys.argv) > 4 else None
    above = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else True

    batch_process(input_folder, output_folder, category=category, price_threshold=price_threshold, above=above)
