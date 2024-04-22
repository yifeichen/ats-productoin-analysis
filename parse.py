import pandas
import requests
from bs4 import BeautifulSoup
import re
import time

urls = {}
data_row = []
domain='https://hoodedhorse.com'
current='https://hoodedhorse.com/wiki/Against_the_Storm/Fabric#Product'
urls[current] = False
for x in range(50):
    print current
    urls[current] = True
    try:
        tables = pandas.read_html(current,match="Buy price")
        result = re.search('Against_the_Storm/(.*)#Product', current)
        name = result.group(1)
        table = tables[0]
        buy_price=table.query("@table[0]=='Buy price'").iat[0,1]
        sell_price=table.query("@table[0]=='Sell value'").iat[0,1]
        data_row.append((name,buy_price,sell_price))
        response = requests.get(current)
        soup = BeautifulSoup(response.content, "html.parser")
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            if "wiki" in url:
                url = domain+url
                if url not in urls.keys():
                    urls[url] = False

        time.sleep(2)
    except Exception as e:
        print "		not found"


    found = False
    for key,value in urls.items():
    	if value is not True:
            current = key
            found = True
            break

    if found is not True:
    	break

print urls

with open("urls.txt", "w") as file1:
    for key,value in urls.items():
        file1.write(key)
        file1.write(' , ')
        file1.write(str(value))
        file1.write("\n")

df = pandas.DataFrame(data_row, columns=['name', 'buy_price', 'sell_price'])
df.set_index(['name'], inplace=True)
df.to_excel("output.xlsx") 
