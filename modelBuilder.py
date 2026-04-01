import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
from collections import Counter
import itertools
import gc

print("1. Loading datasets (Optimized for Laptop Memory)...")
# We force int32 to cut memory usage in half instantly
order_products = pd.read_csv('data/order_products__prior.csv', 
                             usecols=['order_id', 'product_id'],
                             dtype={'order_id': 'int32', 'product_id': 'int32'})
products = pd.read_csv('data/products.csv', 
                       usecols=['product_id', 'product_name'],
                       dtype={'product_id': 'int32'})

print("2. Merging and Grouping into Carts...")
df_merged = pd.merge(order_products, products, on='product_id', how='inner')

# Instantly delete old variables to free up RAM
del order_products, products
gc.collect()

transactions = df_merged.groupby('order_id')['product_name'].apply(list).reset_index(name='items')
del df_merged
gc.collect()

print("3. Sampling 100,000 orders to protect CPU...")
sampled_transactions = transactions['items'].sample(n=100000, random_state=42).tolist()
del transactions
gc.collect()

print("4. Pruning rare items (The crucial step for local execution)...")
item_counts = Counter(itertools.chain.from_iterable(sampled_transactions))

# Item must appear 500 times to be considered
min_occurrences = 500 
popular_items = {item for item, count in item_counts.items() if count >= min_occurrences}
print(f"   -> Reduced unique items to the top {len(popular_items)}")

filtered_transactions = [
    [item for item in transaction if item in popular_items]
    for transaction in sampled_transactions
]
# Drop carts that became empty after pruning
filtered_transactions = [t for t in filtered_transactions if len(t) > 0]

print("5. One-Hot Encoding...")
te = TransactionEncoder()
te_ary = te.fit(filtered_transactions).transform(filtered_transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

del te_ary, sampled_transactions, filtered_transactions
gc.collect()

print("6. Running FP-Growth & Generating Rules...")
frequent_itemsets = fpgrowth(df_encoded, min_support=0.005, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
rules = rules.sort_values(by='lift', ascending=False)

print("7. Saving the engine logic to CSV...")
rules.to_csv('association_rules.csv', index=False)

print("\n Success! Top 5 Cross-Selling Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())