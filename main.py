import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


# Assume a fixed exchange rate (e.g., 1 USD = 280 PKR)
EXCHANGE_RATE_PKR_TO_USD = 280  # You can use live rates with an API later

def convert_pkr_to_usd(pkr_price):
    return round(pkr_price / EXCHANGE_RATE_PKR_TO_USD, 2)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def get_daraz_results(query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.daraz.pk/catalog/?q={query}"
    driver.get(url)
    time.sleep(5)  # Wait for JS to load

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    items = soup.select(".Ms6aG")
    results = []
    for item in items:
        title_tag = item.select_one("a")
        price_tag = item.select_one(".ooOxS")

        if title_tag and price_tag:

            title = title_tag.get("title")
            link = "https:" + title_tag.get("href")
            price_text = price_tag.text.strip().replace(",", "").replace("Rs.", "").replace("₨", "")
            try:
                price_pkr = float(re.findall(r"\d+\.?\d*", price_text)[0])
                price_usd = convert_pkr_to_usd(price_pkr)
                results.append({"title": title, "url": link, "price": price_usd, "original": f"₨{price_pkr:.2f}"})
            except:
                continue

    return results

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
        if title_tag and price_tag:
            title = title_tag.text.strip()
            link = link_tag.get("href")
            # Skip placeholder titles
            if title.lower() == "shop on ebay":
                continue
            price_text = price_tag.text.replace(",", "").replace("$", "")
            try:
                price = float(re.findall(r"\d+\.?\d*", price_text)[0])
                if price < 5:  # Skip unrealistically low prices
                    continue
                results.append({"title": title, "url": link, "price": price, "original": f"${price:.2f}"})
            except:
                continue
    return results


def get_cheapest_two(all_results):
    sorted_items = sorted(all_results, key=lambda x: x["price"])
    return sorted_items[:2]

if __name__ == "__main__":
    user_input = input("Enter product name: ")
    query = user_input.replace(" ", "+")

    print("🔎 Searching Daraz...")
    daraz_results = get_daraz_results(query)
    print(f"✔️ Found {len(daraz_results)} results on Daraz")

    print("🔎 Searching eBay...")
    ebay_results = get_ebay_results(query)
    print(f"✔️ Found {len(ebay_results)} results on eBay")

    all_results = daraz_results + ebay_results
    cheapest_two = get_cheapest_two(all_results)

    print("\n💸 Cheapest 2 Results:")
    for i, item in enumerate(cheapest_two, 1):
        print(f"{i}. {item['title']}\n   {item['original']} (~${item['price']}) - {item['url']}")