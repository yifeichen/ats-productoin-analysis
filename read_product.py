import pandas


def parse_product(url):
    try:
        tables = pandas.read_html(url, match="Buy price")
        table = tables[0]
        buy_price = table.query("@table[0]=='Buy price'").iat[0, 1]
        sell_price = table.query("@table[0]=='Sell value'").iat[0, 1]
        return buy_price, sell_price
    except Exception as e:
        return None, None


def main():
    buy_price, sell_price = parse_product('https://hoodedhorse.com/wiki/Against_the_Storm/Planks#Product')
    print(buy_price)
    print(sell_price)


if __name__ == "__main__":
    main()
