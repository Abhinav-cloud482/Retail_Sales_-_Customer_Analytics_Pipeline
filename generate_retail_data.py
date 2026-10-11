import random
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

num_rows = 2800

# Generate synthetic data components
transaction_ids = [f"TXN-{i:05d}" for i in range(10000, 10000 + num_rows)]
dates = pd.date_range(start="2024-01-01", periods=365, freq="D")
transaction_dates = np.random.choice(dates, num_rows)

customer_ids = [f"CUST-{random.randint(1000, 1500)}" for _ in range(num_rows)]

categories = ["Electronics", "Apparel", "Home & Kitchen", "Sports", "Beauty"]
product_categories = np.random.choice(categories, num_rows, p=[0.2, 0.3, 0.25, 0.15, 0.1])

# Product names mapping based on category
product_dict = {
    "Electronics": ["Wireless Headphones", "Smartwatch", "Bluetooth Speaker", "Power Bank"],
    "Apparel": ["Running Shoes", "Denim Jeans", "Cotton T-Shirt", "Waterproof Jacket"],
    "Home & Kitchen": ["Coffee Maker", "Blender", "Air Fryer", "Non-Stick Pan"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Resistance Bands", "Water Bottle"],
    "Beauty": ["Skincare Kit", "Face Serum", "Hair Dryer", "Lipstick Set"],
}

product_names = [
    random.choice(product_dict[cat]) for cat in product_categories
]
quantities = np.random.randint(1, 5, num_rows)

# Price ranges based on category
price_base = {
    "Electronics": (50, 250),
    "Apparel": (20, 100),
    "Home & Kitchen": (30, 150),
    "Sports": (15, 80),
    "Beauty": (25, 90),
}

unit_prices = [
    round(random.uniform(price_base[cat][0], price_base[cat][1]), 2)
    for cat in product_categories
]
total_sales = [
    round(q * p, 2) for q, p in zip(quantities, unit_prices)
]

regions = ["North", "South", "East", "West", "Central"]
region_col = np.random.choice(regions, num_rows)

payment_methods = ["Credit Card", "PayPal", "Debit Card", "Cash"]
payment_col = np.random.choice(payment_methods, num_rows, p=[0.45, 0.25, 0.2, 0.1])

# Construct DataFrame
df = pd.DataFrame({
    "Transaction_ID": transaction_ids,
    "Date": transaction_dates,
    "Customer_ID": customer_ids,
    "Category": product_categories,
    "Product_Name": product_names,
    "Quantity": quantities,
    "Unit_Price": unit_prices,
    "Total_Sales": total_sales,
    "Region": region_col,
    "Payment_Method": payment_col,
})

# Export to Excel
output_file = "retail_sales_dataset.xlsx"
df.to_excel(output_file, index=False, sheet_name="Sales_Data")

print(
    f"Successfully generated '{output_file}' with {num_rows} rows and {df.shape[1]} columns!"
)