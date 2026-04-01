import pandas as pd

def load_engine(csv_path='association_rules.csv'):
    print("Loading Recommendation Engine...")
    rules = pd.read_csv(csv_path)
    
    # The CSV saves items as strings like "frozenset({'Limes'})"
    # This cleans the text so it's just "Limes"
    rules['antecedents'] = rules['antecedents'].str.replace(r"frozenset\(\{", "", regex=True).str.replace(r"\}\)", "", regex=True).str.replace("'", "")
    rules['consequents'] = rules['consequents'].str.replace(r"frozenset\(\{", "", regex=True).str.replace(r"\}\)", "", regex=True).str.replace("'", "")
    
    return rules

def get_recommendations(item, rules_df, top_n=3):
    # Find rules where the user's item matches the "antecedent" (the IF part)
    # We use 'contains' to handle cases where multiple items are in the set
    match = rules_df[rules_df['antecedents'].str.contains(item, case=False, na=False)]
    
    if match.empty:
        return []
    
    # Sort by Lift (highest statistical strength) and grab the top N consequents
    top_rules = match.sort_values('lift', ascending=False).head(top_n)
    return top_rules['consequents'].tolist()

# --- Run the Virtual Cart ---
if __name__ == "__main__":
    engine_rules = load_engine()
    print(" Engine Loaded successfully.\n")
    
    # Let's test it with the items we know exist from your output
    test_items = ["Limes", "Organic Garlic", "Sparkling Water Grapefruit", "Banana"]
    
    print("--- Testing Virtual Cart Recommendations ---")
    for item in test_items:
        recs = get_recommendations(item, engine_rules)
        if recs:
            print(f" Added to cart: {item}")
            print(f" Frequently Bought Together: {', '.join(recs)}\n")
        else:
            print(f" Added to cart: {item}")
            print(" No strong recommendations found for this item.\n")