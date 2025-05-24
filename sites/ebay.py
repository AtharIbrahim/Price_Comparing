from bs4 import BeautifulSoup
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_ebay_results(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    items = soup.select(".s-item")

    results = []
    for item in items:
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        link_tag = item.select_one("a")

        if not (title_tag and price_tag and link_tag):
            continue
        title = title_tag.text.strip()
        link = link_tag.get("href")
        if title.lower() == "shop on ebay":
            continue
        price_text = price_tag.text.replace(",", "").replace("$", "")
        try:
            price = float(re.findall(r"\d+\.?\d*", price_text)[0])
            if price < 5:
                continue
            results.append({"title": title, "url": link, "price": price, "original": f"${price:.2f}"})
        except:
            continue
    return results
