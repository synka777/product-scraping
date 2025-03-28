"""Scraping Sephora
Copyright (c) 2021 Mathieu BARBE-GAYET
All Rights Reserved.
Released under the MIT license
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import csv


def get_content(driver, url):
    driver.get(url)
    scroll_to_bottom(driver)
    sleep(5)
    return driver.page_source


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


def in_history(url, check_mode=False):
    # Checks if the link has already been processed, if so return True
    with open('./history.log', 'a+', newline='') as file:
        # If the URL is in the history file, quit the function
        if url in file:
            file.close()
            return True
        # If it's not in the history file and if this function has been called without check mode, add it in the history
        if not check_mode:
            file.write(f"{url}\n")
            file.close()
            return True
    # Else if the function is called with check_mode True it will return false.
    # The goal is to use this function to check if an URL has been already processed without adding it in the meantime
    return False


def write_to_csv(url, name, category, price, pros, desc, ingredients, how_to_use, pictures):
    with open('./products.csv', 'a+', newline='') as csv_file:
        if name in csv_file:
            csv_file.close()
            return
        products_csv = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        products_csv.writerow([name, category, price, pros, desc, ingredients, how_to_use, pictures])
        csv_file.close()
        # Adds the URL corresponding to the processed product in the history
        in_history(url)


def get_product_details(driver, url):
    # This function will parse the dom and store each info in a map
    # It then will return this map to the main function
    product_page_dom = get_content(driver, url)

    print(url)
    soup = BeautifulSoup(product_page_dom, 'html.parser')
    script = (soup.find('script', charset=True))
    charset = script['charset']

    # Sets the name
    name = soup.find('span', class_='css-1pgnl76 e65zztl0')
    # print("Name: ", name.text + "\n")
    name = name.text

    # Sets the price
    price = soup.find('b', class_='css-0')
    price_before_discount = soup.find('b', class_='css-vc9b2')
    try:
        # print("Price: ", price.text + "\n")
        price = price.text
    except Exception as e:
        # print("Price: ", price_before_discount.text + "\n")
        price = price_before_discount.text

    # Sets the pros
    pros_found = soup.find_all('img', class_='css-s6sd4y eanm77i0')
    pros = []
    for pro in pros_found:
        # print("Pro: ", pro['alt'] + "\n")
        pros.append(pro['alt'])

    # Sets the description
    description = soup.find('div', class_='css-184tt6k eanm77i0')
    # print("Desc with div and text: ", description.div.text.encode(charset), "\n")
    description = description.div.text.encode(charset)

    # Sets the ingredients
    ingredients = soup.find('div', class_='css-1imcv2s')
    # print("Ingredients: ", ingredients.text.encode(charset), "\n")
    ingredients = ingredients.text.encode(charset)

    # Sets the how to use section
    how_to_use = soup.find(id='howtouse')
    if how_to_use:
        # print(how_to_use.div.div.text.encode(charset))
        how_to_use = how_to_use.div.div.text.encode(charset)

    # Sets a list of pictures
    pictures_found = soup.find_all('img', class_='css-1rovmyu e65zztl0')
    pictures = []
    for picture_link in pictures_found:
        prefix = "https://www.sephora.com"
        if prefix not in picture_link:
            picture_link = f"{prefix}{picture_link['src']}"
        # print("Picture: ", picture['src'] + "\n")
        pictures.append(picture_link)

    # Writes the info found for the product in a CSV file
    write_to_csv(url, name, "Maquillage", price, pros, description, ingredients, how_to_use, pictures)


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
        product_links = get_product_links(a_tags)
        print("Products qty", len(product_links))
        for product_link in product_links:
            href_list_to_scrap.append(product_link)
    for href in href_list_to_scrap:
        # product = get_product_details(driver, href)
        # print(product.encode('utf-8'))
        if not in_history(href, True):
            get_product_details(driver, href)
        else:
            print("Skip: ", href)
    print(len(href_list_to_scrap))
    driver.close()


if __name__ == '__main__':
    main()
