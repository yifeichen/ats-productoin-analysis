import pandas


current='https://hoodedhorse.com/wiki/Against_the_Storm/Planks#Product'
tables = pandas.read_html(current,match="Buy price")
table = tables[0]
buy_price=table.query("@table[0]=='Buy price'").iat[0,1]
sell_price=table.query("@table[0]=='Sell value'").iat[0,1]


print buy_price
print sell_price