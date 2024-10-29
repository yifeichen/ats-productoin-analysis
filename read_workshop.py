from typing import List

import pandas


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
        self.product: IngredientElement = None
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

    def ingredient_expand(self, remain: List[List[IngredientElement]]) -> List[List[IngredientElement]]:
        current_List = remain.pop(0)
        if len(remain) == 0:
            ret = []
            for x in current_List:
                ret.append([x])
            return ret
        else:
            remain_list = self.ingredient_expand(remain)
            ret = []
            for x in current_List:
                for y in remain_list:
                    temp = y.copy()
                    temp.append(x)
                    ret.append(temp)
            return ret

    def expand(self) -> List[List[IngredientElement]]:
        ret = []
        if len(self.ingredient) > 0:
            lines = self.ingredient_expand(self.ingredient)
        else:
            lines = []

        for line in lines:
            line.insert(0, self.product)
            ret.append(line)
        return ret

    def ingredient_list_to_list(self, remain: List[List[IngredientElement]]) -> List:
        current_List = remain.pop(0)
        if len(remain) == 0:
            return [[x.to_string()] for x in current_List]
        else:
            remain_list = self.ingredient_list_to_list(remain)
            if remain_list is None:
                remain_list = []
            ret = []
            for x in current_List:
                for y in remain_list:
                    y.insert(0, x.to_string())
                    ret.append(y)
            return ret

    def to_list(self):
        ret = []
        if len(self.ingredient) > 0:
            lines = self.ingredient_list_to_list(self.ingredient)
        else:
            lines = []

        for line in lines:
            line.insert(0, self.product.to_string())
            ret.append(line)
        return ret


class Workshop:
    def __init__(self):
        self.name = ""
        self.production_chains = []


def parse_ingredient_list(str_list) -> List[IngredientElement]:
    ret = []
    while len(str_list) >= 2:
        p = IngredientElement()
        p.number = int(str_list.pop(0))
        p.name = str_list.pop(0)
        while len(str_list) > 0 and not str_list[0].isdigit():
            p.name += " " + str_list.pop(0)
        if p.name != "-":
            ret.append(p)
    return ret


def parse_workshop(url) -> Workshop:
    tables = pandas.read_html(url, match="Ingredient")
    table = tables[0]
    building_name = url.split('/')[-1]
    data_rows = table.query(f'Building=="{building_name.replace("_", " ")}"')
    ret = Workshop()
    ret.name = building_name

    print(f"trying to parse {building_name}")

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
        time_string = row.iloc[1].replace("★", "")
        current.time = int(time_string[:-3]) * 60 + int(time_string[-2:])
        for row_index in range(2, len(data_rows.count()) - 1):
            ing_str_list = row.iloc[row_index].replace("\xa0", " ").split()
            ing_list = parse_ingredient_list(ing_str_list)
            if len(ing_list) > 0:
                current.ingredient.append(ing_list)
        ret.production_chains.append(current)
    return ret


def main():
    workshop = parse_workshop('https://hoodedhorse.com/wiki/Against_the_Storm/Cooperage')
    for production in workshop.production_chains:
        for x in production.expand():
            line = ""
            for y in x:
                line += y.to_string() + " "
            print(line)

if __name__ == "__main__":
    main()
