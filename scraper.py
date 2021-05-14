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
        """if "skuId" in url:
            expand_info(driver, "css-1n34gja eanm77i0")
            expand_info(driver, "css-1o99c9n eanm77i0")"""
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("New height: ", new_height)
        if new_height == last_height:
            break
        else:
            last_height = new_height
            sleep(5)


"""def expand_info(driver, class_name):
    try:
        expand_info_buttons = driver.find_element_by_class_name(class_name)
        for button in expand_info_buttons:
            if not button['aria-expanded']:
                button.click()
                continue
            if button['aria-expanded'] == "false":
                button.click()
    except Exception as e:
        print("Unable to find a button with class name ", class_name, ": ", e)"""


def get_content(driver, url):
    driver.get(url)
    scroll_to_bottom(driver)
    sleep(5)
    return driver.page_source


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


def get_product_details(driver, url):
    # This function will parse the dom and store each info in a map
    # It then will return this map to the main function
    product_page_dom = get_content(driver, url)
    try:
        print(url)
        soup = BeautifulSoup(product_page_dom, 'html.parser')
        title = soup.find('span', class_='css-1pgnl76 e65zztl0')
        print("Title: ", title.text + "\n")
        price = soup.find('b', class_='css-0')
        print("Price: ", price.text + "\n")
        pros = soup.find_all('img', class_='css-s6sd4y eanm77i0')
        for pro in pros:
            print("Pro: ", pro['alt'] + "\n")
        description = soup.find('div', class_='css-184tt6k eanm77i0')
        print("Description: ", description.text + "\n")
        ingredients = soup.find('div', class_='css-1imcv2s')
        print("Ingredients: ", ingredients.text + "\n")
        how_to_use = soup.find(id='howtouse')
        # print("How to use: ", how_to_use.children, "\n")
        for stuff in how_to_use.children:
            print(stuff)
        pictures = soup.find_all('img', class_='css-1rovmyu e65zztl0')
        for picture in pictures:
            print("Picture: ", picture['src'] + "\n")

    except Exception as e:
        print("Error: Something went wrong when build the product object: ", e)

    # return


def main():
    urls_to_scrape = [
        # "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=1",
        # "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=2",
        # "https://www.sephora.com/ca/fr/shop/foundation-makeup?currentPage=3",
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
        # product = get_product_details(driver, href)
        get_product_details(driver, href)
        # print(product.encode('utf-8'))
    print(len(href_list_to_scrap))
    driver.close()


if __name__ == '__main__':
    main()
