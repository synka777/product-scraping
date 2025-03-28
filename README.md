
# Product Scraping

## 🔍 Overview

This Python script scrapes product information from Sephora's website using Selenium and BeautifulSoup. The extracted data includes product names, prices, descriptions, ingredients, and images, which are stored in a CSV file.

## 🍜 Features

- Uses Selenium to handle dynamic page loading
- Extracts product details such as:
    - Name
    - Price
    - Description
    - Ingredients
    - Pros
    - Usage instructions
    - Images
- Saves extracted data to a CSV file
- Avoids duplicate scraping using a history log

## 📄 Requirements

### Dependencies

Ensure you have the following Python libraries installed:

```bash
pip install -r requirements.txt
```

### WebDriver

This script requires a WebDriver for Selenium (e.g., GeckoDriver for Firefox). Download it from [the official repo for GeckoDriver](https://github.com/mozilla/geckodriver/releases)

Then place it in the script's directory.

## 🚀 Usage

To start scraping Sephora products, run:

```bash
python scraper.py
```

## ⬇️ Output

- Product data: Stored in products.csv
- Processed URLs: Logged in history.log to prevent duplicate scraping