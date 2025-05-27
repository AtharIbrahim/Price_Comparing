# 🛒 Price Comparing Tool (BargainBot)

A smart Python-based price comparison tool that takes a product name as input, searches multiple e-commerce websites (like **eBay**, **Daraz**, and **Amazon**), fetches the available listings, and shows the **2 lowest-priced products** along with their **direct links**.

---

## 🚀 Features

- 🔍 Accepts user input for product search
- 🌐 Searches across:
  - eBay
  - Daraz
  - Amazon
- 📉 Compares prices and fetches only the **two lowest-priced** options
- 🔗 Displays clickable product links
- ⚡ Fast and efficient with minimal user input

---

## 📸 Demo

![demo](https://github.com/AtharIbrahim/Price_Comparing/blob/main/screenshots/frontend1.png)

---

## 🧠 How It Works

1. User inputs the product name (e.g., "Samsung Galaxy S21").
2. Script scrapes e-commerce sites for matching product listings.
3. Prices are extracted and sorted.
4. The two lowest-priced products are returned with their URLs.

---

## 🛠️ Tech Stack

- Python
- `requests`, `BeautifulSoup` for web scraping
- `pandas` for organizing and sorting results
- `re` for text cleaning and processing

---

## 📦 Installation

```bash
git clone https://github.com/AtharIbrahim/Price_Comparing.git
cd Price_Comparing
pip install -r requirements.txt
```

## ▶️ Usage
```bash
python main.py
```

## 📌 Notes

- The accuracy of results depends on the product's availability and website structure.

- Some websites may have anti-scraping mechanisms; using headers/user agents helps bypass basic protections.

## 📬 Contact
<ul>
  <li><strong>Name</strong>: Athar Ibrahim Khalid</li>
  <li><strong>GitHub</strong>: <a href="https://github.com/AtharIbrahim/" target="_blank">https://github.com/AtharIbrahim/</a></li>
  <li><strong>LinkedIn</strong>: <a href="https://www.linkedin.com/in/athar-ibrahim-khalid-0715172a2/" target="_blank">LinkedIn Profile</a></li>
  <li><strong>Website</strong>: <a href="https://atharibrahimkhalid.netlify.app/" target="_blank">Athar Ibrahim Khalid</a></li>
</ul>


## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
