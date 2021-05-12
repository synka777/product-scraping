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
    href_list_to_scrap = []
    for url in urls_to_scrape:
        a_tags = []
        while len(a_tags) < 12:
            dom = get_content(url)
            a_tags = get_a_tags(dom)
        product_links = get_product_links(a_tags)
        for product_link in product_links:
            href_list_to_scrap.append(product_link)
    for href in href_list_to_scrap:
        print(href)
    print(len(href_list_to_scrap))


if __name__ == '__main__':
    main()
