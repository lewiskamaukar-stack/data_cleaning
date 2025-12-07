import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time

def get_products_from_page(url):
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "lxml")
        products = []
        cards = soup.find_all("article", class_="prd")

        for card in cards:
            name_tag = card.find("div", class_="name")
            price_tag = card.find("div", class_="prc")
            link_tag = card.find("a")
            image_tag = card.find("img")

            name = name_tag.text.strip() if name_tag else ""
            price_text = price_tag.text.strip() if price_tag else ""
            price = int(price_text.replace("KSh", "").replace(",", "").strip()) if price_text else None
            link = "https://www.jumia.co.ke" + link_tag.get("href", "") if link_tag else ""
            image = image_tag.get("src", "") if image_tag else ""

            # Skip product if name or price is missing
            if not name or price is None:
                continue

            products.append({
                "name": name,
                "price": price,
                "link": link,
                "image": image
            })

        return products
    except:
        return []

def scrape_jumia_category(category, max_pages, price_alert=None):
    all_products = []
    print(f"Starting scrape for '{category}' ({max_pages} pages)...\n")
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}/{max_pages}...")
        url = f"https://www.jumia.co.ke/{category}/?page={page}"
        products = get_products_from_page(url)
        all_products.extend(products)
        time.sleep(1)

    if not all_products:
        print("No valid products found.")
        return

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"output/jumia_{category}_{timestamp}.xlsx"

    df = pd.DataFrame(all_products)
    if price_alert:
        df["price_alert"] = df["price"] <= price_alert

    with pd.ExcelWriter(excel_file) as writer:
        df.to_excel(writer, index=False, sheet_name="Products")
        if price_alert:
            df[df["price_alert"]].to_excel(writer, index=False, sheet_name="Price Alert")

    print(f"\nScraping complete! {len(all_products)} valid products saved to '{excel_file}'")
    if price_alert:
        print(f"{df['price_alert'].sum()} products under KSh {price_alert} flagged.")

if __name__ == "__main__":
    print("==== JUMIA AUTOMATED SCRAPER ====")
    category = input("Enter category (e.g., smartphones, laptops): ").strip()
    max_pages = input("Enter number of pages to scrape (e.g., 5): ").strip()
    price_alert = input("Enter price alert threshold (optional, e.g., 15000): ").strip()

    try:
        max_pages = int(max_pages)
    except:
        max_pages = 5
    try:
        price_alert = int(price_alert) if price_alert else None
    except:
        price_alert = None

    scrape_jumia_category(category, max_pages, price_alert)


