from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from HTML

EXCHANGE_RATE_PKR_TO_USD = 280

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
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    items = soup.select(".Ms6aG")
    results = []
    for item in items:
        title_tag = item.select_one(".RfADt a")
        price_tag = item.select_one(".ooOxS")

        if title_tag and price_tag:
            title = title_tag.text.strip()
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

def get_cheapest_two(all_results):
    return sorted(all_results, key=lambda x: x["price"])[:2]

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify([])

    daraz = get_daraz_results(query)
    ebay = get_ebay_results(query)
    all_results = daraz + ebay
    return jsonify(get_cheapest_two(all_results))

if __name__ == "__main__":
    app.run(debug=True)
