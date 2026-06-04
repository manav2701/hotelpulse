from prophet import Prophet
import pandas as pd

def fit_prophet(df, hotel_type: str = "City Hotel"):
    hotel_df = df[df['hotel'] == hotel_type][['week', 'occupancy_rate']].copy()
    hotel_df.columns = ['ds', 'y']
    hotel_df['ds'] = pd.to_datetime(hotel_df['ds']).dt.tz_localize(None)

    m = Prophet(weekly_seasonality=True, yearly_seasonality=True, changepoint_prior_scale=0.05)
    m.fit(hotel_df)

    future = m.make_future_dataframe(periods=8, freq='W')
    forecast = m.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
