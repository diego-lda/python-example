import pandas as pd
import folium
from folium.plugins import HeatMap
import seaborn as sns
from scikit-learn.model_selection import train_test_split
from scikit-learn.preprocessing import StandardScaler
from scikit-learn.pipeline import make_pipeline
from scikit-learn.linear_model import Ridge
from scikit-learn.metrics import mean_squared_error
import numpy as np

# Load the CSV file
file_path = '/Users/diegolara/guidance/live_example/python-example/data/master_sales.csv'
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
    if pd.notnull(row['shop_latitude']) and pd.notnull(row['buyer_age'])
]

# Add a heatmap layer to the map
HeatMap(heat_data, radius=15, max_zoom=10).add_to(m)

# Plotting buyers age against sale payment using a violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='sale_payment', y='shop_hours_start', data=df, palette=['yellow', 'green'])
plt.title('Distribution of Sale Payments by Buyer Age')
plt.xlabel('Buyer Age')
plt.ylabel('Sale Payment')
plt.show()

# Save the map to an HTML file and provide instructions to view it
m.save("data/sales_heatmap.html")
print("Choropleth map saved as sales_heatmap.html. Open this file in your browser to view the map.")


# Select features and target variable
features = ['buyer_age', 'shop_hours_start', 'shop_hours_end', 'sale_volume']
target = 'sale_price'

# Drop rows with missing values in the selected features or target
df = df.dropna(subset=features + [target])

# Split the data into training and testing sets
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with standard scaling and Ridge regression
pipeline = make_pipeline(StandardScaler(), Ridge(alpha=1.0))

# Fit the model
pipeline.fit(X_train, y_train)

# Predict on the test set
y_pred = pipeline.predict(X_test)

# Calculate and print the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Print the coefficients of the model
coefficients = pipeline.named_steps['ridge'].coef_
print("Coefficients:")
for feature, coef in zip(features, coefficients):
    print(f"{feature}: {coef:.4f}")