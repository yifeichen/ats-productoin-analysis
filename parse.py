from typing import List, Set

import pandas
import requests
from bs4 import BeautifulSoup
from read_product import parse_product
from read_workshop import parse_workshop, ProductionChain, Workshop
import re
import time
import os

cwd = os.getcwd()
print(f"current directory {cwd}")

urls = set()
visited_url = set()
product_prices = []
work_shops: List[Workshop] = []
domain = 'https://hoodedhorse.com'
current = 'https://hoodedhorse.com/wiki/Against_the_Storm/Cooperage'
urls.add(current)
for x in range(550):

    if len(urls) == 0:
        print("read all links")
        break

    current = urls.pop()
    visited_url.add(current)
    
    try:
        parse_product_detect = False
        try:
            result = re.search('Against_the_Storm/(.*)', current)
            name = result.group(1)
            buy_price, sell_price = parse_product(current)
            if buy_price is not None:
                parse_product_detect = True
                product_prices.append([name, buy_price, sell_price])
                print(f" {current}	product")
        except Exception as e:
            parse_product_detect = False
            print(e)

        if not parse_product_detect:
            parse_workshop_detect = False
            try:
                result = re.search('Against_the_Storm/(.*)', current)
                name = result.group(1)
                workshop = parse_workshop(current)
                if len(workshop.production_chains) > 0:
                    work_shops.append(workshop)
                    parse_workshop_detect = True
                    print(f" {current}	workshop")
            except Exception as e:
                parse_workshop_detect = False
                print(e)

        if not parse_product_detect and not parse_workshop_detect:
            print(f" {current}	parse not working")
            time.sleep(1)
            continue

        response = requests.get(current)
        soup = BeautifulSoup(response.content, "html.parser")
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            url_split = url.split("/")
            if len(url_split) > 2 and url_split[1] == "wiki" and "index" not in url and ":" not in url:
                url = domain + url.replace("#Product", "").replace("#Ingredient", "")
                if url not in visited_url:
                    urls.add(url)

        time.sleep(1)
    except Exception as e:
        print(current + "  not found")

with open("urls.txt", "w") as visited_log:
    for url in visited_url:
        visited_log.write(url)
        visited_log.write("\n")

df_prices = pandas.DataFrame(product_prices, columns=['name', 'buy_price', 'sell_price'])

production_row = []
index = 2
for workshop in work_shops:
    for chain in workshop.production_chains:
        for c in chain.expand():
            row = [workshop.name, chain.time]
            for ing in c:
                row.append(ing.number)
                row.append(ing.name)
            while len(row) < 10:
                row.append(0)
                row.append(None)
            row.append(f"=IFNA(VLOOKUP(D{index},prices!A2:prices!C100,2,1),0)")
            row.append(f"=IFNA(VLOOKUP(F{index},prices!A2:prices!C100,2,1),0)")
            row.append(f"=IFNA(VLOOKUP(H{index},prices!A2:prices!C100,2,1),0)")
            row.append(f"=IFNA(VLOOKUP(J{index},prices!A2:prices!C100,2,1),0)")
            row.append(f"=E{index}*L{index}+G{index}*M{index}+I{index}*N{index}")
            row.append(f"=C{index}*K{index}-O{index}")
            index += 1
            production_row.append(row)

df_production = pandas.DataFrame(production_row,
                                 columns=['name', "time", 'product_name', 'product_number', "ing1number", "ing1name",
                                          "ing2number", "ing2name", "ing3number", "ing3name", "productCost", "ing1cost",
                                          "ing2cost", "ing3cost", "ingcost", "profit"])

writer = pandas.ExcelWriter('output.xlsx', engine='xlsxwriter')
df_prices.to_excel(writer, sheet_name='prices', index=False)
df_production.to_excel(writer, sheet_name='production', index=False)

writer.close()
