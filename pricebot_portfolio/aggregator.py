
import os
import pandas as pd
from scrapers import jumia, kilimall, ebay_api
from dotenv import load_dotenv

load_dotenv()

PRODUCTS = [
    {"shop": "Jumia", "url": "https://www.jumia.co.ke/example-product-page"},
    {"shop": "Kilimall", "url": "https://www.kilimall.co.ke/example-product-page"},
    {"shop": "eBay", "item_id": "v1|2**********2|0"},
]

def main():
    rows = []
    for p in PRODUCTS:
        try:
            if p['shop'] == 'Jumia':
                rows.append(jumia.scrape_product(p['url']))
            elif p['shop'] == 'Kilimall':
                rows.append(kilimall.scrape_product(p['url']))
            elif p['shop'] == 'eBay':
                token = os.getenv('EBAY_OAUTH_TOKEN')
                if not token:
                    raise RuntimeError("Set EBAY_OAUTH_TOKEN in .env")
                rows.append(ebay_api.get_item_by_id(p['item_id'], token))
        except Exception as e:
            rows.append({"shop": p.get('shop'), "error": str(e), "url": p.get('url', p.get('item_id'))})

    df = pd.DataFrame(rows)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    df['shipping'] = df['shipping'].fillna(0)
    df['total_price'] = df['price'] + df['shipping']

    if not df.empty:
        idx = df['total_price'].idxmin()
        df['is_cheapest'] = False
        df.loc[idx, 'is_cheapest'] = True

    out = "comparison.xlsx"
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Comparison")
        summary = df.loc[df['is_cheapest']].head(1)[['shop','name','total_price','url']]
        summary.to_excel(writer, index=False, sheet_name="Summary")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
