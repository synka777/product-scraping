"""Scraping Sephora
Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

"""def store_data(dom):
    try:
        pass
    except Exception as e:
        print("Error: Something went wrong when trying to store data locally: ", e)"""


# function to handle dynamic page content loading - using Selenium
def scroll_to_bottom(driver):
    # define initial page height for 'while' loop
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("New height: ", new_height)
        if new_height == last_height:
            break
        else:
            last_height = new_height
            sleep(5)


def get_content(driver, url):
    try:
        driver.get(url)
        scroll_to_bottom(driver)
        sleep(5)
        return driver.page_source
    except Exception as e:
        print("Error: Something went wrong when getting the content accessible from", url, "Details: ", e)


def get_a_tags(dom):
    try:
        soup = BeautifulSoup(dom, 'html.parser')
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
    driver = webdriver.Firefox(executable_path="./geckodriver.exe")
    href_list_to_scrap = []
    for url in urls_to_scrape:
        a_tags = []
        while len(a_tags) < 12:
            dom = get_content(driver, url)
            a_tags = get_a_tags(dom)
            print("A tags qty: ", len(a_tags))
        product_links = get_product_links(a_tags)
        print("Products qty", len(product_links))
        for product_link in product_links:
            href_list_to_scrap.append(product_link)
    for href in href_list_to_scrap:
        print(href)
    print(len(href_list_to_scrap))
    driver.close()


if __name__ == '__main__':
    main()
