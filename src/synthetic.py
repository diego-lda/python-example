import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

fake = Faker('en_GB')

# Helper functions
def generate_shop_hours():
    start_hour = np.random.poisson(8)
    end_hour = start_hour + np.random.poisson(9)
    start_time = f"{start_hour:02d}:00"
    end_time = f"{min(end_hour, 23):02d}:00"
    return start_time, end_time

def generate_release_date():
    base_date = datetime.now() - timedelta(days=random.randint(0, 365*10))
    return base_date.strftime("%d-%m-%Y")

# Table 1: Information on shops
shops = []
for i in range(1, 101):
    shop_id = i
    shop_geography = fake.local_latlng(country_code = 'GB')
    shop_latitude = shop_geography[0]
    shop_longitude = shop_geography[1]
    shop_location = shop_geography[2]
    shop_name = fake.company()
    shop_type = random.choice(['small', 'medium', 'large'])
    shop_hours_start, shop_hours_end = generate_shop_hours()
    open_sunday = random.choices([0, 1], weights=[0.6, 0.4], k=1)[0]
    shops.append([shop_id, shop_location, shop_latitude, shop_longitude, shop_name, shop_type, shop_hours_start, shop_hours_end, open_sunday])

shops_df = pd.DataFrame(shops, columns=['shop_id', 'shop_location', 'shop_latitude', 'shop_longitude', 'shop_name', 'shop_type', 'shop_hours_start', 'shop_hours_end', 'open_sunday'])

# Table 2: Information on Items
items = []
item_classes = ['kitchen', 'bedroom', 'outdoors', 'vehicles', 'furniture', 'technology', 'books', 'clothes']
for i in range(1, 201):
    item_id = i
    item_name = fake.word()
    item_weight = round(random.uniform(0.1, 10.0), 2)
    item_class = random.choice(item_classes)
    item_release_date = generate_release_date()
    item_brand = fake.company()
    item_price = round(random.uniform(5.0, 500.0), 2)
    items.append([item_id, item_name, item_weight, item_class, item_release_date, item_brand, item_price])

items_df = pd.DataFrame(items, columns=['item_id', 'item_name', 'item_weight', 'item_class', 'item_release_date', 'item_brand', 'item_price'])

# Table 3: Information of sales
sales = []
for i in range(1, 100001):
    shop_id = random.choice(shops_df['shop_id'])
    item_id = random.choice(items_df['item_id'])
    sale_id = i
    sale_time = fake.date_time_between(start_date='-5y', end_date='now')
    item_price = items_df.loc[items_df['item_id'] == item_id, 'item_price'].values[0]
    sale_price = round(item_price + np.random.normal(0, 5), 2)
    sale_number = random.randint(1, 10)
    sale_volume = sale_price * sale_number
    buyer_age = random.randint(18, 80)
    buyer_sex = random.choice(['M', 'F'])
    sale_payment = random.choice(['phone', 'credit', 'debit', 'cash'])
    sales.append([shop_id, item_id, sale_id, sale_time, sale_price, sale_number, sale_volume, buyer_age, buyer_sex, sale_payment])

sales_df = pd.DataFrame(sales, columns=['shop_id', 'item_id', 'sale_id', 'sale_time', 'sale_price', 'sale_number', 'sale_volume', 'buyer_age', 'buyer_sex', 'sale_payment'])

# Save to CSV
shops_df.to_csv('data/raw_shops.csv', index=False)
items_df.to_csv('data/raw_items.csv', index=False)
sales_df.to_csv('data/raw_sales.csv', index=False)