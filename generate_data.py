import json
import csv
import random
from datetime import datetime, timedelta

# Config
NUM_ORDERS = 800
NUM_CUSTOMERS = 100

# Generate customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    name = f"Customer_{i}" if random.random() > 0.1 else ""  # 10% empty names
    city = random.choice(["NY", "LA", "SF", "TX", "CHI"])
    
    customers.append({
        "customer_id": i,
        "name": name,
        "city": city
    })

# Save customers.csv
with open("customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "name", "city"])
    writer.writeheader()
    writer.writerows(customers)

# Generate orders
orders = []
start_date = datetime(2024, 1, 1)

for i in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    
    # 10% invalid amount
    amount = random.randint(50, 1000) if random.random() > 0.1 else None
    
    date = start_date + timedelta(days=random.randint(0, 10))

    orders.append({
        "order_id": i,
        "customer_id": customer_id,
        "amount": amount,
        "date": date.strftime("%Y-%m-%d")
    })

# Save orders.json
with open("orders.json", "w") as f:
    json.dump(orders, f, indent=2)

print("✅ Data generated successfully!")