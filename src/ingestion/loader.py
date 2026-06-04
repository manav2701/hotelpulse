import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/hotel_bookings.csv")
EVENTS_PATH = Path("data/raw/events_calendar.csv")

def load_bookings() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    # Drop rows with null values in key columns
    df = df.dropna(subset=['children', 'country', 'agent'])
    # Parse arrival date
    df['arrival_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + '-' +
        df['arrival_date_month'] + '-' +
        df['arrival_date_day_of_month'].astype(str),
        format='%Y-%B-%d'
    )
    return df

def load_events() -> pd.DataFrame:
    df = pd.read_csv(EVENTS_PATH, parse_dates=['date'])
    return df
