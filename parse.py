from typing import List

import pandas
import requests
from bs4 import BeautifulSoup
from read_product import parse_product
from read_workshop import parse_workshop, ProductionChain, Workshop
import re
import time

urls = {}
product_prices = []
work_shops: List[Workshop] = []
domain = 'https://hoodedhorse.com'
current = 'https://hoodedhorse.com/wiki/Against_the_Storm/Cooperage'
urls[current] = False
for x in range(550):
    found = False
    for key, value in urls.items():
        if value == False:
            found = True
            current = key
            break

    if not found:
        print("read all links")
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
                product_prices.append([name, buy_price, sell_price])
                print(f" {current}	product")
        except Exception as e:
            parse_product_detect = False


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
                if url not in urls.keys():
                    urls[url] = False

        time.sleep(1)
    except Exception as e:
        print(current + "	not found")


with open("urls.txt", "w") as file1:
    for key, value in urls.items():
        file1.write(key)
        file1.write(' , ')
        file1.write(str(value))
        file1.write("\n")


df = pandas.DataFrame(product_prices, columns=['name', 'buy_price', 'sell_price'])

production_row = []
index=2
for workshop in work_shops:
    for chain in workshop.production_chains:
        for c in chain.expand():
            row = []
            row.append(workshop.name)
            row.append(chain.time)
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

df1 = pandas.DataFrame(production_row, columns=['name', "time" ,'product_name', 'product_number',"ing1number","ing1name","ing2number","ing2name","ing3number","ing3name", "productCost", "ing1cost", "ing2cost", "ing3cost", "ingcost", "profit"])



writer = pandas.ExcelWriter('output.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='prices', index=False)
df1.to_excel(writer, sheet_name='production', index=False)


writer.close()
