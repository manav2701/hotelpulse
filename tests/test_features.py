import pandas as pd
from src.features.engineer import engineer_weekly_features, get_feature_columns

def test_engineer_weekly_features(sample_bookings, sample_events):
    sample_bookings['arrival_date'] = pd.to_datetime('2024-01-01')
    dfs = []
    for i in range(10):
        df = sample_bookings.copy()
        df['arrival_date'] = pd.to_datetime('2024-01-01') + pd.Timedelta(weeks=i)
        dfs.append(df)
    
    large_bookings = pd.concat(dfs)
    weekly = engineer_weekly_features(large_bookings, sample_events)
    
    assert not weekly.empty
    assert 'occupancy_rate' in weekly.columns
    assert 'rolling_avg_4w' in weekly.columns
    
    features = get_feature_columns()
    for f in features:
        assert f in weekly.columns
