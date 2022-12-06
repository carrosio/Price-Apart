import pandas as pd

data_df = pd.read_json('data/scraped_apartments.json')
dolar_price = 320

def to_pesos(row):
    if row['price_currency'] == 'U$S':
        value = row['price'] * dolar_price
    else:
        value = row['price']
    return value

data_df['count'] = 1
data_df['price_pesos'] = data_df.apply(to_pesos, axis=1)
data_df['price_pesos_plus_expenses'] = data_df.price_pesos + data_df.expenses
data_df['m2'] = data_df.price_pesos_plus_expenses / data_df.total_covered
data_df['price_plus_expenses_USD'] = data_df.price_pesos_plus_expenses / dolar_price
data_df['price_plus_expenses_USD_m2'] = data_df.price_plus_expenses_USD / data_df.total_covered

print(data_df)