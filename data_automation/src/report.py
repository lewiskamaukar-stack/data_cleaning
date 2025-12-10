import pandas as pd
import matplotlib.pyplot as plt

def summary(df):
    return df.describe(include="all")

def chart(df, chart_path):
    num = df.select_dtypes(include="number").columns
    if len(num):
        df[num[0]].plot(kind="bar")
        plt.savefig(chart_path)
        plt.close()

def excel_report(df, summary_df, out):
    with pd.ExcelWriter(out) as w:
        df.to_excel(w, "Cleaned", index=False)
        summary_df.to_excel(w, "Summary")
