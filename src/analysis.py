import pandas as pd

# Load the CSV file
file_path = '/Users/diegolara/guidance/python-example/src/master_sales.csv'
df = pd.read_csv(file_path)

# Perform some interesting analysis
# Example: Calculate total sales, average sales, and sales by region

# Total sales
total_sales = df['Sales'].sum()
print(f"\nTotal Sales: ${total_sales:,.2f}")

# Average sales
average_sales = df['Sales'].mean()
print(f"Average Sales: ${average_sales:,.2f}")

# Sales by region
sales_by_region = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print("\nSales by Region:")
print(sales_by_region)

# Additional analysis: Sales trend over time
df['Date'] = pd.to_datetime(df['Date'])
sales_trend = df.groupby(df['Date'].dt.to_period('M'))['Sales'].sum()
print("\nSales Trend Over Time:")
print(sales_trend)

# Plotting the sales trend
import matplotlib.pyplot as plt

sales_trend.plot(kind='line', title='Sales Trend Over Time', xlabel='Date', ylabel='Sales')
plt.show()