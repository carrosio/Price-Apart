def message(msj):
    return print(msj.upper())

def to_pesos(row, dollar_price):
    if row['price_currency'] == 'U$S':
        value = row['price'] * dollar_price
    else:
        value = row['price']
    return value