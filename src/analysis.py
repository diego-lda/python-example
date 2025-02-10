import pandas as pd
import folium
from folium.plugins import HeatMap

# Load the CSV file
file_path = '/Users/diegolara/guidance/python-example/data/master_sales.csv'
df = pd.read_csv(file_path)

# Perform some interesting analysis
# Example: Calculate total sales, average sales, and sales by region

# Total sales
total_sales = df['sale_volume'].sum()
print(f"\nTotal Sales: £{total_sales:,.2f}")

# Average sale price
average_sales = df['sale_volume'].mean()
print(f"Average Sales: £{average_sales:,.2f}")

# Sales by location
sales_by_region = df.groupby('shop_location')['sale_price'].sum().sort_values(ascending=False)
print("\nSales by Location:")
print(sales_by_region)

# Additional analysis: Sales trend over time
df['sale_time'] = pd.to_datetime(df['sale_time'])  # Ensure sale_time is in datetime format
sales_trend = df.groupby(df['sale_time'].dt.to_period('M'))['sale_price'].sum()
print("\nSales Trend Over Time:")
print(sales_trend)

# Plotting the sales trend
import matplotlib.pyplot as plt

sales_trend.plot(kind='line', title='Sales Trend Over Time', xlabel='Date', ylabel='Sales')
plt.show()

# Calculate the center of the map using the mean latitude and longitude
map_center = [df['shop_latitude'].mean(), df['shop_longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=6)

# Prepare data for the heatmap: each point is [latitude, longitude, weight (sale_price)]
heat_data = [
    [row['shop_latitude'], row['shop_longitude'], row['sale_price']]
    for index, row in df.iterrows()
    if pd.notnull(row['shop_latitude']) and pd.notnull(row['shop_longitude'])
]

# Add a heatmap layer to the map
HeatMap(heat_data, radius=15, max_zoom=10).add_to(m)

# Save the map to an HTML file and provide instructions to view it
m.save("data/sales_heatmap.html")
print("Choropleth map saved as sales_heatmap.html. Open this file in your browser to view the map.")