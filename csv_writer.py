import pandas as pd

def save_products(products):
    df = pd.DataFrame(products)
    df.to_csv("data/products.csv", index=False, encoding="utf-8")
    print("CSV saved with", len(products), "products")