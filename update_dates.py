import pandas as pd

df = pd.read_csv('data/raw/events_calendar.csv')
# Change all dates from 2024 to 2026
df['date'] = df['date'].str.replace('2024', '2026')
df.to_csv('data/raw/events_calendar.csv', index=False)
print("Updated events calendar to 2026")
