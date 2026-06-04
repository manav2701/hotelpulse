import pandas as pd
import numpy as np

def engineer_weekly_features(bookings_df: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate bookings into weekly demand features.
    Target: weekly occupancy rate (proxy = non-canceled bookings / total bookings)
    """
    df = bookings_df.copy()

    # Filter to non-canceled only for demand signal
    df['week'] = df['arrival_date'].dt.to_period('W').dt.start_time

    # Weekly aggregations
    weekly = df.groupby(['week', 'hotel']).agg(
        total_bookings=('is_canceled', 'count'),
        cancellations=('is_canceled', 'sum'),
        avg_adr=('adr', 'mean'),
        avg_lead_time=('lead_time', 'mean'),
        special_requests=('total_of_special_requests', 'mean'),
        repeated_guests=('is_repeated_guest', 'mean'),
    ).reset_index()

    weekly['occupancy_rate'] = (
        (weekly['total_bookings'] - weekly['cancellations']) / weekly['total_bookings']
    ).clip(0, 1)

    # Time features
    weekly['week_of_year'] = pd.to_datetime(weekly['week']).dt.isocalendar().week.astype(int)
    weekly['month'] = pd.to_datetime(weekly['week']).dt.month
    weekly['quarter'] = pd.to_datetime(weekly['week']).dt.quarter
    weekly['is_weekend_heavy'] = weekly['week_of_year'].apply(
        lambda w: 1 if w in [1, 13, 17, 26, 35, 40, 52] else 0
    )

    # Merge events
    events_df['week'] = events_df['date'].dt.to_period('W').dt.start_time
    event_weekly = events_df.groupby('week')['demand_multiplier'].max().reset_index()
    weekly = weekly.merge(event_weekly, on='week', how='left')
    weekly['demand_multiplier'] = weekly['demand_multiplier'].fillna(1.0)

    # Lag features (previous week occupancy)
    weekly = weekly.sort_values('week')
    weekly['occupancy_lag_1'] = weekly.groupby('hotel')['occupancy_rate'].shift(1)
    weekly['occupancy_lag_2'] = weekly.groupby('hotel')['occupancy_rate'].shift(2)
    weekly['rolling_avg_4w'] = weekly.groupby('hotel')['occupancy_rate'].transform(
        lambda x: x.shift(1).rolling(4).mean()
    )

    weekly = weekly.dropna()
    return weekly

def get_feature_columns() -> list:
    return [
        'week_of_year', 'month', 'quarter', 'is_weekend_heavy',
        'avg_adr', 'avg_lead_time', 'special_requests', 'repeated_guests',
        'demand_multiplier', 'occupancy_lag_1', 'occupancy_lag_2', 'rolling_avg_4w'
    ]
