from typing import List

import pandas
import requests
from bs4 import BeautifulSoup
from read_product import parse_product
from read_workshop import parse_workshop, ProductionChain
import re
import time

urls = {}
product_prices = []
productionChains: List[ProductionChain] = []
domain = 'https://hoodedhorse.com'
current = 'https://hoodedhorse.com/wiki/Against_the_Storm/Cooperage'
urls[current] = False
for x in range(550):
    for key, value in urls.items():
        if value == False:
            current = key
            break
    urls[current] = True
    try:
        parse_product_detect = False
        try:
            result = re.search('Against_the_Storm/(.*)', current)
            name = result.group(1)
            buy_price, sell_price = parse_product(current)
            if buy_price is not None:
                parse_product_detect = True
                product_prices.append((name, buy_price, sell_price))
                print(f" {current}	product")
        except Exception as e:
            parse_product_detect = False


        parse_workshop_detect = False
        try:
            result = re.search('Against_the_Storm/(.*)', current)
            name = result.group(1)
            chains = parse_workshop(current)
            if len(chains) > 0:
                productionChains.append(chains)
                parse_workshop_detect = True
                print(f" {current}	workshop")
        except Exception as e:
            parse_workshop_detect = False

        if not parse_product_detect and not parse_workshop_detect:
            print(f" {current}	parse not working")
            time.sleep(2)
            continue

        response = requests.get(current)
        soup = BeautifulSoup(response.content, "html.parser")
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            url_split = url.split("/")
            if len(url_split) > 2 and url_split[1] == "wiki" and "index" not in url and ":" not in url:
                url = domain + url.replace("#Product", "").replace("#Ingredient", "")
                if url not in urls.keys():
                    urls[url] = False

        time.sleep(2)
    except Exception as e:
        print(current + "	not found")

    found = False
    for key, value in urls.items():
        if value is not True:
            current = key
            found = True
            break

    if found is not True:
        break


with open("urls.txt", "w") as file1:
    for key, value in urls.items():
        file1.write(key)
        file1.write(' , ')
        file1.write(str(value))
        file1.write("\n")

#df = pandas.DataFrame(product_prices, columns=['name', 'buy_price', 'sell_price'])
#df.set_index(['name'], inplace=True)
#df.to_excel("output.xlsx")



with open("productionchain.txt", "w") as file1:
    for chains in productionChains:
        for chain in chains:
            file1.write(f"{chain.name} \n")
            file1.write(f"{chain.to_string()}")
            file1.write("\n")
            file1.write("\n")
    file1.write("\n")

with open("prices.txt", "w") as file2:
    for p in product_prices:
        file2.write(str(p)+"\n")
