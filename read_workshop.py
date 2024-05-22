from typing import List

import pandas
import requests
from bs4 import BeautifulSoup
import re


class IngredientElement:
    def __init__(self):
        self.number = None
        self.name = None

    def to_string(self):
        return f" {self.number} {self.name}"


class ProductionChain:
    def __init__(self):
        self.product:IngredientElement = None
        self.ingredient1:List[IngredientElement] = None
        self.ingredient2:List[IngredientElement] = None

    def to_string(self):
        ret = ""
        lines = []
        if len(self.ingredient1) > 0 and len(self.ingredient2) > 0:
            for ing1 in self.ingredient1:
                for ing2 in self.ingredient2:
                    lines.append(f"{ing1.to_string()} + {ing2.to_string()}")

        else:
            if len(self.ingredient1) > 0:
                for ing1 in self.ingredient1:
                    lines.append(ing1.to_string())
            else:
                for ing2 in self.ingredient2:
                    lines.append(ing2.to_string())

        for line in lines:
            ret += self.product.to_string() + " : " + line + "\n"

        return ret





def parse_ingredient_list(strList):
    ret = []
    while len(strList) >= 2:
        p = IngredientElement()
        p.number = int(strList.pop(0))
        p.name = strList.pop(0)
        while len(strList) > 0 and not strList[0].isdigit():
            p.name += " " + strList.pop(0)
        ret.append(p)
    return ret


def parse_workshop(url):
    tables = pandas.read_html(url, match="Ingredient")
    table = tables[0]
    building_name = url.split('/')[-1]
    data_rows = table.query(f'Building=="{building_name.replace("_"," ")}"')
    ret = []

    for index, row in data_rows.iterrows():
        productList = row['Product'].replace("\xa0", " ").split()
        ing1List = row[2].replace("\xa0", " ").split()
        ing2List = row[3].replace("\xa0", " ").split()
        current = ProductionChain()
        p = IngredientElement()
        p.number = int(productList.pop(0))
        p.name = productList.pop(0)
        current.product = p
        current.ingredient1 = parse_ingredient_list(ing1List)
        current.ingredient2 = parse_ingredient_list(ing2List)
        ret.append(current)
    return ret


def main():
    productions = parse_workshop('https://hoodedhorse.com/wiki/Against_the_Storm/Flawless_Leatherworker')
    for production in productions:
        print(production.to_string())


if __name__ == "__main__":
    main()
