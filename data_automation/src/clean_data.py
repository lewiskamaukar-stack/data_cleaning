import pandas as pd
import argparse

def clean_csv(input_path, output_path):
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.drop_duplicates().fillna("N/A")
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    clean_csv(args.input, args.output)
