from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_amazon_results(query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    items = soup.select("div.s-main-slot div.s-result-item[data-component-type='s-search-result']")

    results = []
    for item in items:
        title_tag = item.select_one("h2 a span")
        link_tag = item.select_one("h2 a")
        price_whole = item.select_one("span.a-price-whole")
        price_fraction = item.select_one("span.a-price-fraction")

        if not (title_tag and price_whole and price_fraction and link_tag):
            continue

        title = title_tag.text.strip()
        link = "https://www.amazon.com" + link_tag.get("href")
        try:
            price = float(price_whole.text.replace(",", "") + "." + price_fraction.text)
            results.append({"title": title, "url": link, "price": price, "original": f"${price:.2f}"})
        except:
            continue

    return results
