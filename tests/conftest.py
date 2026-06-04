import pytest
import pandas as pd

@pytest.fixture
def sample_bookings():
    return pd.DataFrame({
        'hotel': ['City Hotel', 'City Hotel', 'Resort Hotel'],
        'is_canceled': [0, 1, 0],
        'lead_time': [10, 20, 5],
        'arrival_date_year': [2024, 2024, 2024],
        'arrival_date_month': ['January', 'January', 'January'],
        'arrival_date_week_number': [1, 1, 1],
        'arrival_date_day_of_month': [1, 5, 10],
        'stays_in_weekend_nights': [1, 0, 2],
        'stays_in_week_nights': [2, 1, 5],
        'adults': [2, 1, 2],
        'children': [0, 0, 1],
        'country': ['USA', 'UK', 'UAE'],
        'agent': [9, 9, 14],
        'adr': [100.0, 150.0, 200.0],
        'total_of_special_requests': [1, 0, 2],
        'is_repeated_guest': [0, 0, 1]
    })

@pytest.fixture
def sample_events():
    return pd.DataFrame({
        'date': pd.to_datetime(['2024-01-01', '2024-02-14']),
        'event_name': ["New Year's", "Valentine's"],
        'event_type': ["public_holiday", "social_event"],
        'demand_multiplier': [1.4, 1.3]
    })
