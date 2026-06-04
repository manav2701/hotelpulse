import xgboost as xgb
import mlflow
import mlflow.xgboost
import joblib
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.features.engineer import get_feature_columns

FEATURES = get_feature_columns()
TARGET = 'occupancy_rate'
MODEL_PATH = "artifacts/model.pkl"

def train(df, hotel_type: str = "City Hotel"):
    hotel_df = df[df['hotel'] == hotel_type].sort_values('week')
    X = hotel_df[FEATURES]
    y = hotel_df[TARGET]

    tscv = TimeSeriesSplit(n_splits=3)

    with mlflow.start_run(run_name=f"xgboost_{hotel_type.replace(' ', '_')}"):
        params = {
            "n_estimators": 200,
            "learning_rate": 0.05,
            "max_depth": 5,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "random_state": 42,
            "n_jobs": 4
        }
        mlflow.log_params(params)

        model = xgb.XGBRegressor(**params)
        maes = []

        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
            preds = model.predict(X_val)
            maes.append(mean_absolute_error(y_val, preds))

        final_mae = np.mean(maes)
        mlflow.log_metric("cv_mae", final_mae)
        mlflow.log_metric("cv_mae_pct", final_mae * 100)

        # Final fit on all data
        model.fit(X, y)
        mlflow.xgboost.log_model(model, "model")
        
        import os
        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        print(f"✅ Model trained | CV MAE: {final_mae:.4f} ({final_mae*100:.1f}%)")
        return model

def predict_next_weeks(model, latest_row: dict, n_weeks: int = 4) -> list:
    """Generate rolling forecasts for next N weeks."""
    import pandas as pd
    forecasts = []
    current = latest_row.copy()

    for i in range(n_weeks):
        X = pd.DataFrame([{f: current.get(f, 0) for f in FEATURES}])
        pred = float(model.predict(X)[0])
        pred = max(0.0, min(1.0, pred))
        forecasts.append(pred)
        # Roll lag features forward
        current['occupancy_lag_2'] = current['occupancy_lag_1']
        current['occupancy_lag_1'] = pred
        current['week_of_year'] = (current['week_of_year'] % 52) + 1
        current['month'] = ((current['month']) % 12) + 1
    return forecasts
