import pandas


def parse_product(url):
    try:
        tables = pandas.read_html(url, match="Value when sold")
        df = tables[0]
        buy_price = df[df.iloc[:, 2] == "Value when sold"].iloc[:, 0].values
        sell_price = df[df.iloc[:, 2] == "Traders' price"].iloc[:, 0].values
        return buy_price, sell_price
    except Exception as e:
        print(e)
        return None, None


def main():
    buy_price, sell_price = parse_product('https://hoodedhorse.com/wiki/Against_the_Storm/Planks#Product')
    print(buy_price)
    print(sell_price)


if __name__ == "__main__":
    main()
