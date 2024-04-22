import requests
from bs4 import BeautifulSoup


urls =  set()
buy = {}
sell = {}

current='https://hoodedhorse.com/wiki/Against_the_Storm/Fabric#Product'

response = requests.get(current)
soup = BeautifulSoup(response.content, "html.parser")
link_elements = soup.select("a[href]")
for link_element in link_elements:
    url = link_element['href']
    if "#Product" in url:
        urls.add(url)



print urls