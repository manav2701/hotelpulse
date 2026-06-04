import pytest
import pandas as pd
from src.models.xgboost_model import train, predict_next_weeks
from src.features.engineer import get_feature_columns

def test_xgboost_train_and_predict():
    weeks = pd.date_range(start='2024-01-01', periods=20, freq='W')
    data = []
    for w in weeks:
        row = {
            'week': w,
            'hotel': 'City Hotel',
            'occupancy_rate': 0.7,
        }
        for f in get_feature_columns():
            row[f] = 1.0
        data.append(row)
        
    df = pd.DataFrame(data)
    
    model = train(df, hotel_type='City Hotel')
    assert model is not None
    
    latest = df.iloc[-1].to_dict()
    forecasts = predict_next_weeks(model, latest, n_weeks=4)
    assert len(forecasts) == 4
    for f in forecasts:
        assert 0.0 <= f <= 1.0
