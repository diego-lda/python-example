import pandas as pd

# Read in the raw data
sales = pd.read_csv('/Users/diegolara/guidance/python-example/data/raw_sales.csv')
shops = pd.read_csv('/Users/diegolara/guidance/python-example/data/raw_shops.csv')
items = pd.read_csv('/Users/diegolara/guidance/python-example/data/raw_items.csv')

# Merge sales with shop information
sales_extended = pd.merge(sales, shops, on='shop_id', how='left')

# Merge the extended sales table with item information
master_sales = pd.merge(sales_extended, items, on='item_id', how='left')

# Save the master table
master_sales.to_csv('/Users/diegolara/guidance/python-example/data/master_sales.csv', index=False)