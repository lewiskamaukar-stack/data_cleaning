import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jumia_smartphones():
    url = "https://www.jumia.co.ke/smartphones/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    products = []
    cards = soup.find_all("article", class_="prd")

    for card in cards:
        name = card.find("div", class_="name")
        price = card.find("div", class_="prc")
        link = card.find("a")
        image = card.find("img")

        products.append({
            "name": name.text.strip() if name else "",
            "price": price.text.strip() if price else "",
            "link": "https://www.jumia.co.ke" + link["href"] if link else "",
            "image": image["src"] if image else ""
        })

    df = pd.DataFrame(products)
    df.to_csv("output/jumia_products.csv", index=False)
    print("Scraping complete! Saved to output/jumia_products.csv")

if __name__ == "__main__":
    scrape_jumia_smartphones()

