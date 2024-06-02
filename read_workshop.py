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
        self.time: int = 0
        self.name = ""
        self.product: IngredientElement = []
        self.ingredient: List[List[IngredientElement]] = []

    def to_string(self):
        ret = ""
        if len(self.ingredient) > 0:
            lines = self.ingredient_list_to_string(self.ingredient)
        else:
            lines = [""]

        for line in lines:
            ret += self.product.to_string() + " : " + str(self.time) + " : " + line + "\n"
        return ret

    def ingredient_list_to_string(self, remain: List[List[IngredientElement]]) -> List[str]:
        current_List = remain.pop(0)
        if len(remain) == 0:
            return [x.to_string() for x in current_List]
        else:
            remain_list = self.ingredient_list_to_string(remain)
            ret = []
            for x in current_List:
                ret.extend([x.to_string() + " " + y for y in remain_list])
            return ret



def parse_ingredient_list(strList) -> List[IngredientElement]:
    ret = []
    while len(strList) >= 2:
        p = IngredientElement()
        p.number = int(strList.pop(0))
        p.name = strList.pop(0)
        while len(strList) > 0 and not strList[0].isdigit():
            p.name += " " + strList.pop(0)
        if p.name != "-":
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
        current = ProductionChain()
        current.name = building_name
        p = IngredientElement()
        p.number = int(productList.pop(0))
        p.name = productList.pop(0)
        while len(productList) > 0 and not productList[0].isdigit():
            p.name += " " + productList.pop(0)
        current.product = p
        time_string = row[1].replace("★", "")
        current.time = int(time_string[:-3]) * 60 + int(time_string[-2:])
        for index in range(2,len(data_rows.count())-1):
            ing_str_list = row[index].replace("\xa0", " ").split()
            ing_list = parse_ingredient_list(ing_str_list)
            if len(ing_list)>0:
                current.ingredient.append(ing_list)
        ret.append(current)
    return ret


def main():
    productions = parse_workshop(' https://hoodedhorse.com/wiki/Against_the_Storm/Hallowed_Herb_Garden')
    for production in productions:
        print(production.to_string())


if __name__ == "__main__":
    main()
