import pandas as pd

# 1. Load the data from the 'data' folder 
# (Reading a subset of 1 million rows for initial testing to save RAM)
print("Loading data...")
order_products = pd.read_csv('data/order_products__prior.csv', nrows=1000000) 
products = pd.read_csv('data/products.csv')

# 2. Merge tables to get human-readable product names
print("Merging data...")
df_merged = pd.merge(
    order_products, 
    products[['product_id', 'product_name']], 
    on='product_id', 
    how='left'
)

# 3. Group by order_id to create transactions
# This converts rows of individual items into a list of items per order
print("Grouping into transactions...")
transactions = df_merged.groupby('order_id')['product_name'].apply(list).reset_index(name='items')

# 4. Display the transformed data
print("\n--- Data Ready for FP-Growth ---")
print(transactions.head())