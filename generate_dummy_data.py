import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import os

os.makedirs('data/raw', exist_ok=True)
np.random.seed(42)
n = 1000

dates = [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n)]
hotel = np.random.choice(['City Hotel', 'Resort Hotel'], n)
is_canceled = np.random.choice([0, 1], n, p=[0.7, 0.3])
lead_time = np.random.randint(1, 200, n)
adr = np.random.uniform(50, 300, n)
children = np.random.choice([0, 1, 2], n, p=[0.8, 0.15, 0.05])
country = np.random.choice(['USA', 'UK', 'UAE', 'FRA'], n)
agent = np.random.randint(1, 100, n)
special_requests = np.random.choice([0, 1, 2], n, p=[0.7, 0.2, 0.1])
repeated = np.random.choice([0, 1], n, p=[0.9, 0.1])

df = pd.DataFrame({
    'hotel': hotel,
    'is_canceled': is_canceled,
    'lead_time': lead_time,
    'arrival_date_year': [d.year for d in dates],
    'arrival_date_month': [d.strftime('%B') for d in dates],
    'arrival_date_week_number': [d.isocalendar()[1] for d in dates],
    'arrival_date_day_of_month': [d.day for d in dates],
    'stays_in_weekend_nights': np.random.randint(0, 3, n),
    'stays_in_week_nights': np.random.randint(1, 6, n),
    'adults': np.random.randint(1, 4, n),
    'children': children,
    'country': country,
    'agent': agent,
    'adr': adr,
    'total_of_special_requests': special_requests,
    'is_repeated_guest': repeated
})

df.to_csv('data/raw/hotel_bookings.csv', index=False)
print("Dummy data generated at data/raw/hotel_bookings.csv")
