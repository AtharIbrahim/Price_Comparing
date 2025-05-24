from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

EXCHANGE_RATE_PKR_TO_USD = 280

def convert_pkr_to_usd(pkr_price):
    return round(pkr_price / EXCHANGE_RATE_PKR_TO_USD, 2)

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
