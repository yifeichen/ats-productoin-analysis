import pandas
import requests
from bs4 import BeautifulSoup

current='https://hoodedhorse.com/wiki/Against_the_Storm/Cooperage'
#tables = pandas.read_html(current,match="Ingredient")
#table = tables[0]
#table.set_index('Building', inplace=True)
#ing=table.query('Building=="Cooperage"')

#print tables
response = requests.get(current)
soup = BeautifulSoup(response.content, 'html.parser')
lst = soup.find_all('table', recursive=False)

print lst