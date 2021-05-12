"""Scraping Sephora
Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license
"""
from bs4 import BeautifulSoup
import requests
import lxml


"""def store_data(dom):
    try:
        pass
    except Exception as e:
        print("Error: Something went wrong when trying to store data locally: ", e)"""


def get_content(url):
    try:
        return requests.get(url)
    except Exception as e:
        print("Error: Something went wrong when getting the content accessible from", url, "Details: ", e)


def get_a_tags(dom):
    try:
        soup = BeautifulSoup(dom.content, 'html.parser')
        return soup.find_all('a', class_='css-ix8km1')
    except Exception as e:
        print("Error: Something went wrong when getting the <a> tags: ", e)


def get_product_links(a_tags):
    links = []
    for a_tag in a_tags:
        link = a_tag['href']
        prefix = "https://www.sephora.com"
        if prefix not in link:
            link = f"{prefix}{link}"
        links.append(link)
    return links


def main():
    urls_to_scrape = [
        "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
        "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
        "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
        "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=4"
    ]
    for url in urls_to_scrape:
        print(url)
        a_tags = []
        while len(a_tags) < 12:
            dom = get_content(url)
            if dom:
                a_tags = get_a_tags(dom)
                print(len(a_tags))
            else:
                print("No dom")
            """product_pages = get_product_pages(product_links)
            print(product_pages)"""
        product_links = get_product_links(a_tags)
        print("Product links LEN: ", len(product_links))
        print(product_links)


if __name__ == '__main__':
    main()
