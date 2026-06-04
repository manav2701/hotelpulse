# 🏨 HotelPulse — Full Build Plan
### Dynamic Demand Forecasting Engine + LLM Marketing Trigger
> Hybrid: Original architecture inspired by renswickd/MLOps-Hotel-Revenue-Management structure

---

## 📌 What You're Building

A **production-deployed** ML system that:
1. Ingests hotel booking + external demand signal data
2. Forecasts weekly occupancy demand (XGBoost + Prophet)
3. Detects anomalies / demand dips automatically
4. Triggers an LLM agent to generate targeted marketing copy
5. Displays everything on a live Streamlit dashboard
6. Is tracked via MLflow, containerized via Docker, deployed on Render

**Public URL on Render = goes directly on your resume.**

---

## 🗂️ Final Project Structure

```
hotelpulse/
│
├── data/
│   ├── raw/                          # Downloaded datasets (gitignored)
│   │   ├── hotel_bookings.csv        # Kaggle dataset
│   │   └── events_calendar.csv       # UAE public holidays (manual CSV)
│   └── processed/
│       ├── weekly_features.csv       # Engineered feature matrix
│       └── predictions.csv           # Model output
│
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py                 # Load & validate raw CSVs
│   │   └── external.py              # Fetch weather + events APIs
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineer.py              # All feature engineering logic
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── xgboost_model.py         # XGBoost forecaster
│   │   ├── prophet_model.py         # Prophet trend model
│   │   └── evaluate.py              # Metrics + MLflow logging
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   └── marketing_agent.py       # LLM alert trigger logic
│   │
│   └── pipeline/
│       ├── __init__.py
│       └── run_pipeline.py          # Orchestrates full run
│
├── dashboard/
│   └── app.py                       # Streamlit UI (main entry point)
│
├── config/
│   └── config.yaml                  # Thresholds, model params, API keys ref
│
├── mlruns/                          # MLflow experiment tracking (auto-generated)
│
├── artifacts/
│   └── model.pkl                    # Saved trained model
│
├── tests/
│   └── test_features.py             # Basic unit tests
│
├── .env                             # API keys (gitignored)
├── .gitignore
├── requirements.txt
├── Dockerfile
├── render.yaml                      # Render deployment config
└── README.md
```

---

## 🔴 MANUAL SETUP — Things You Must Do Yourself

> These cannot be vibe-coded. Do these FIRST before touching any code.

---

### MANUAL TASK 1 — Download the Kaggle Dataset

**Time: 5 minutes**

1. Go to: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
2. Sign in / create free Kaggle account
3. Download `hotel_bookings.csv` (~8MB, 119k rows)
4. Place it at: `data/raw/hotel_bookings.csv`

**What's in it:**
- `arrival_date_year`, `arrival_date_month`, `arrival_date_week_number`
- `lead_time`, `adr` (average daily rate), `is_canceled`
- `market_segment`, `meal`, `reserved_room_type`
- `stays_in_weekend_nights`, `stays_in_week_nights`
- `hotel` (City Hotel vs Resort Hotel)

This is your **primary training data.** 119k bookings, two hotel types, 2015–2017.

---

### MANUAL TASK 2 — Get an OpenWeatherMap API Key (Free)

**Time: 5 minutes**

Used to pull historical + forecast weather as a demand signal (weather affects travel bookings).

1. Go to: https://openweathermap.org/api
2. Sign up free
3. Go to "API Keys" in your account
4. Copy your key
5. Add to `.env`:
```
OPENWEATHER_API_KEY=your_key_here
```

**Free tier gives you:** 1,000 calls/day — more than enough.

---

### MANUAL TASK 3 — Get an API Key for LLM (Claude or OpenAI)

**Time: 5 minutes**

This powers the marketing alert agent.

**Option A — Anthropic (Claude) [Recommended]:**
1. Go to: https://console.anthropic.com
2. Create account → API Keys → Create Key
3. Add to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

**Option B — OpenAI:**
1. Go to: https://platform.openai.com/api-keys
2. Add to `.env`:
```
OPENAI_API_KEY=your_key_here
```

**Cost:** Tiny. Running the agent once costs < $0.01. Budget $2–3 for testing.

---

### MANUAL TASK 4 — Create the UAE Events Calendar CSV

**Time: 10 minutes**

This is a simple CSV you build manually — UAE public holidays and peak travel events. This is what makes your model UAE-aware and hospitality-specific (generic models don't have this).

Create `data/raw/events_calendar.csv`:

```csv
date,event_name,event_type,demand_multiplier
2024-01-01,New Year's Day,public_holiday,1.4
2024-02-14,Valentine's Day,social_event,1.3
2024-03-29,Eid Al Fitr Start,public_holiday,1.6
2024-04-01,Eid Al Fitr End,public_holiday,1.6
2024-04-18,UAE National Sports Day,public_holiday,1.2
2024-06-05,Eid Al Adha Start,public_holiday,1.5
2024-09-15,Dubai Shopping Festival,tourism_event,1.4
2024-10-31,Halloween,social_event,1.2
2024-11-15,Dubai Airshow,business_event,1.5
2024-11-28,Thanksgiving,tourism_event,1.3
2024-12-01,UAE National Day,public_holiday,1.5
2024-12-20,Christmas Period Start,tourism_event,1.6
2024-12-31,New Year's Eve,social_event,1.8
```

Add more rows as needed. The `demand_multiplier` is used as a feature — you're saying "during this event, expected demand is X times baseline."

---

### MANUAL TASK 5 — Set Up Render Account

**Time: 10 minutes (do this at the END when code is ready)**

1. Go to: https://render.com
2. Sign up with GitHub (so it can access your repo)
3. When deploying: New → Web Service → Connect your GitHub repo
4. Set environment variables in Render dashboard (paste your `.env` values there)
5. Render will auto-detect your `Dockerfile` and build it

**Free tier limitations:** Spins down after 15 min inactivity (cold start ~30s). Fine for a demo/portfolio.

---

### MANUAL TASK 6 — Set Up MLflow Tracking (Local First)

**Time: 5 minutes**

MLflow runs locally during dev. For production on Render, the `mlruns/` folder gets written inside the container (ephemeral, fine for demo). If you want persistent tracking, use MLflow's free hosted tier at https://dagshub.com (optional).

For now, just install it — it works out of the box:
```bash
pip install mlflow
mlflow ui  # opens at localhost:5000
```

---

## 🟡 HYBRID ARCHITECTURE DECISIONS

> Where we borrow from `renswickd` vs where we go original

| Component | renswickd approach | HotelPulse approach | Why different |
|---|---|---|---|
| Model | LightGBM (cancellation) | XGBoost + Prophet (demand) | Forecasting ≠ classification |
| Pipeline | GCP-native | Cloud-agnostic Python | Render deployment, no GCP needed |
| Frontend | Flask + HTML | Streamlit | 5x faster to build, better charts |
| CI/CD | Jenkins | GitHub Actions | Simpler, free, integrates with Render |
| Data | Single CSV | CSV + Weather API + Events CSV | Richer signal = better story |
| New layer | None | LLM marketing agent | The differentiator |
| Deployment | GCP App Engine | Render (Docker) | Free tier, simpler |

We **keep** from renswickd:
- MLflow experiment tracking pattern
- Docker + requirements.txt structure
- Feature selection approach (use their `utils/` as reference)
- The pipeline orchestration pattern (`run_pipeline.py`)

---

## 🟢 BUILD PLAN — Hour by Hour

---

### ⏱ HOUR 1 (0:00–1:00) — Environment + Data + Features

#### Step 1.1 — Project setup (15 min)
```bash
mkdir hotelpulse && cd hotelpulse
python -m venv venv && source venv/bin/activate
git init
```

Create `requirements.txt`:
```
pandas==2.1.0
numpy==1.24.0
scikit-learn==1.3.0
xgboost==2.0.0
prophet==1.1.4
mlflow==2.8.0
streamlit==1.28.0
plotly==5.17.0
anthropic==0.20.0
requests==2.31.0
python-dotenv==1.0.0
pyyaml==6.0.1
joblib==1.3.2
pytest==7.4.0
```

```bash
pip install -r requirements.txt
```

Create `.env`:
```
ANTHROPIC_API_KEY=
OPENWEATHER_API_KEY=
ALERT_THRESHOLD=0.65
```

Create `.gitignore`:
```
.env
data/raw/
mlruns/
artifacts/
venv/
__pycache__/
*.pkl
```

---

#### Step 1.2 — Data loader (20 min)

`src/ingestion/loader.py`:
```python
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
        df['arrival_date_day_of_month'].astype(str)
    )
    return df

def load_events() -> pd.DataFrame:
    df = pd.read_csv(EVENTS_PATH, parse_dates=['date'])
    return df
```

`src/ingestion/external.py`:
```python
import requests, os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

def fetch_weather_signal(city: str = "Dubai", days_back: int = 90) -> dict:
    """Fetch historical avg temperature as demand proxy."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    # Use current weather as a stand-in signal for demo
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    resp = requests.get(url, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        return {"temp": data['main']['temp'], "condition": data['weather'][0]['main']}
    return {"temp": 28.0, "condition": "Clear"}  # fallback for demo
```

---

#### Step 1.3 — Feature engineering (25 min)

`src/features/engineer.py`:
```python
import pandas as pd
import numpy as np

def engineer_weekly_features(bookings_df: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate bookings into weekly demand features.
    Target: weekly occupancy rate (proxy = non-canceled bookings / total bookings)
    """
    df = bookings_df.copy()

    # Filter to non-canceled only for demand signal
    df['week'] = df['arrival_date'].dt.to_period('W').apply(lambda r: r.start_time)

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
    events_df['week'] = events_df['date'].dt.to_period('W').apply(lambda r: r.start_time)
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
```

---

### ⏱ HOUR 2 (1:00–2:00) — ML Models + MLflow

#### Step 2.1 — XGBoost Forecaster (30 min)

`src/models/xgboost_model.py`:
```python
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
            "random_state": 42
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
```

#### Step 2.2 — Prophet for trend line (15 min)

`src/models/prophet_model.py`:
```python
from prophet import Prophet
import pandas as pd

def fit_prophet(df, hotel_type: str = "City Hotel"):
    hotel_df = df[df['hotel'] == hotel_type][['week', 'occupancy_rate']].copy()
    hotel_df.columns = ['ds', 'y']
    hotel_df['ds'] = pd.to_datetime(hotel_df['ds'])

    m = Prophet(weekly_seasonality=True, yearly_seasonality=True, changepoint_prior_scale=0.05)
    m.fit(hotel_df)

    future = m.make_future_dataframe(periods=8, freq='W')
    forecast = m.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
```

#### Step 2.3 — Pipeline orchestrator (15 min)

`src/pipeline/run_pipeline.py`:
```python
from src.ingestion.loader import load_bookings, load_events
from src.features.engineer import engineer_weekly_features
from src.models.xgboost_model import train
from pathlib import Path
import pandas as pd

def run():
    print("🔄 Loading data...")
    bookings = load_bookings()
    events = load_events()

    print("⚙️  Engineering features...")
    weekly = engineer_weekly_features(bookings, events)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    weekly.to_csv("data/processed/weekly_features.csv", index=False)

    print("🤖 Training model...")
    model = train(weekly, hotel_type="City Hotel")

    print("✅ Pipeline complete.")
    return weekly, model

if __name__ == "__main__":
    run()
```

---

### ⏱ HOUR 3 (2:00–3:00) — LLM Agent + Streamlit Dashboard

#### Step 3.1 — Marketing Alert Agent (20 min)

`src/agents/marketing_agent.py`:
```python
import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_marketing_alert(
    predicted_occupancy: float,
    week_label: str,
    hotel_type: str,
    threshold: float = 0.65
) -> dict:
    """
    Called when predicted occupancy drops below threshold.
    Returns generated marketing copy in multiple formats.
    """
    if predicted_occupancy >= threshold:
        return {"triggered": False, "message": None}

    gap = threshold - predicted_occupancy
    urgency = "high" if gap > 0.15 else "medium"

    prompt = f"""You are a luxury hotel marketing strategist for a 5-star hotel in Dubai (similar to FIVE Hotels).

Context:
- Hotel type: {hotel_type}
- Week: {week_label}
- Predicted occupancy: {predicted_occupancy:.0%}
- Target occupancy threshold: {threshold:.0%}
- Demand gap: {gap:.0%} below target
- Urgency level: {urgency}

Generate a marketing response package with exactly this JSON structure:
{{
  "whatsapp_message": "2-sentence luxury flash deal for UAE residents (max 160 chars)",
  "email_subject": "compelling subject line for a targeted re-engagement email",
  "instagram_caption": "luxury lifestyle caption with 3 relevant hashtags",
  "recommended_discount": "specific % discount or package offer",
  "target_segment": "which guest segment to target (e.g. UAE residents, GCC travelers, business travelers)"
}}

Tone: luxury, aspirational, exclusive — never cheap or desperate. Think Ritz-Carlton, not budget hotel."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    try:
        content = message.content[0].text
        # Extract JSON from response
        start = content.find('{')
        end = content.rfind('}') + 1
        result = json.loads(content[start:end])
        result["triggered"] = True
        result["predicted_occupancy"] = predicted_occupancy
        return result
    except Exception as e:
        return {
            "triggered": True,
            "error": str(e),
            "raw": message.content[0].text
        }
```

---

#### Step 3.2 — Streamlit Dashboard (40 min)

`dashboard/app.py`:
```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import joblib
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.loader import load_bookings, load_events
from src.features.engineer import engineer_weekly_features, get_feature_columns
from src.models.xgboost_model import predict_next_weeks
from src.models.prophet_model import fit_prophet
from src.agents.marketing_agent import generate_marketing_alert

# ── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HotelPulse",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500&display=swap');
    
    .main { background-color: #0a0a0a; }
    .block-container { padding-top: 2rem; }
    
    h1 { font-family: 'Playfair Display', serif !important; color: #C9A84C !important; }
    h2, h3 { font-family: 'Inter', sans-serif !important; }
    
    .metric-card {
        background: #181818;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .alert-box {
        background: linear-gradient(135deg, #1a0a0a, #2a1515);
        border: 1px solid #8B2020;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .marketing-card {
        background: #111827;
        border: 1px solid #1E3A5F;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏨 HotelPulse")
    st.markdown("*Demand Forecasting Engine*")
    st.divider()

    hotel_type = st.selectbox("Property Type", ["City Hotel", "Resort Hotel"])
    forecast_weeks = st.slider("Forecast Horizon (weeks)", 2, 8, 4)
    alert_threshold = st.slider("Alert Threshold (occupancy %)", 50, 85, 65) / 100

    st.divider()
    st.markdown("**Model Info**")
    st.caption("Algorithm: XGBoost + Prophet")
    st.caption("Data: Hotel Booking Demand Dataset")
    st.caption("Tracking: MLflow")

# ── Load & Cache Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    bookings = load_bookings()
    events = load_events()
    weekly = engineer_weekly_features(bookings, events)
    return weekly

@st.cache_resource
def load_model():
    try:
        return joblib.load("artifacts/model.pkl")
    except:
        return None

# ── Main Content ──────────────────────────────────────────────────────────────
st.title("🏨 HotelPulse")
st.markdown("##### Dynamic Demand Forecasting & Marketing Intelligence")
st.divider()

with st.spinner("Loading data and model..."):
    weekly = load_data()
    model = load_model()

hotel_df = weekly[weekly['hotel'] == hotel_type].sort_values('week')

# ── KPI Row ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

recent = hotel_df.tail(4)
current_occ = hotel_df['occupancy_rate'].iloc[-1]
avg_occ = hotel_df['occupancy_rate'].mean()
avg_adr = hotel_df['avg_adr'].mean()
trend = hotel_df['occupancy_rate'].iloc[-1] - hotel_df['occupancy_rate'].iloc[-5]

with col1:
    st.metric("Current Occupancy", f"{current_occ:.1%}", f"{trend:+.1%} vs 4w ago")
with col2:
    st.metric("Avg Occupancy (All Time)", f"{avg_occ:.1%}")
with col3:
    st.metric("Avg Daily Rate", f"${avg_adr:.0f}")
with col4:
    alert_status = "🔴 Alert Zone" if current_occ < alert_threshold else "🟢 On Target"
    st.metric("Status", alert_status)

st.divider()

# ── Forecast Section ──────────────────────────────────────────────────────────
st.subheader("📈 Demand Forecast")

# Generate forecasts
if model:
    latest_row = hotel_df[get_feature_columns()].iloc[-1].to_dict()
    forecasts = predict_next_weeks(model, latest_row, n_weeks=forecast_weeks)
else:
    # Fallback demo forecasts
    import numpy as np
    forecasts = [avg_occ + np.random.uniform(-0.1, 0.1) for _ in range(forecast_weeks)]

# Build forecast dates
last_date = pd.to_datetime(hotel_df['week'].iloc[-1])
forecast_dates = [last_date + pd.Timedelta(weeks=i+1) for i in range(forecast_weeks)]
forecast_df = pd.DataFrame({
    'week': forecast_dates,
    'occupancy_rate': forecasts,
    'type': 'Forecast'
})

# Historical (last 12 weeks)
hist_df = hotel_df.tail(12)[['week', 'occupancy_rate']].copy()
hist_df['week'] = pd.to_datetime(hist_df['week'])
hist_df['type'] = 'Historical'

# Prophet trend
prophet_forecast = fit_prophet(weekly, hotel_type)

# Plot
fig = go.Figure()

# Historical line
fig.add_trace(go.Scatter(
    x=hist_df['week'], y=hist_df['occupancy_rate'],
    name='Historical Occupancy',
    line=dict(color='#C9A84C', width=2),
    mode='lines+markers'
))

# Forecast line
fig.add_trace(go.Scatter(
    x=forecast_df['week'], y=forecast_df['occupancy_rate'],
    name='XGBoost Forecast',
    line=dict(color='#5A9BE0', width=2, dash='dot'),
    mode='lines+markers'
))

# Prophet trend
fig.add_trace(go.Scatter(
    x=pd.to_datetime(prophet_forecast['ds']),
    y=prophet_forecast['yhat'],
    name='Prophet Trend',
    line=dict(color='#4CAF7D', width=1.5, dash='dash'),
    opacity=0.7
))

# Confidence band
fig.add_trace(go.Scatter(
    x=pd.concat([
        pd.to_datetime(prophet_forecast['ds']),
        pd.to_datetime(prophet_forecast['ds'])[::-1]
    ]),
    y=pd.concat([prophet_forecast['yhat_upper'], prophet_forecast['yhat_lower'][::-1]]),
    fill='toself',
    fillcolor='rgba(76, 175, 125, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Prophet CI',
    showlegend=True
))

# Alert threshold line
fig.add_hline(
    y=alert_threshold,
    line_dash="dot",
    line_color="#E05A5A",
    annotation_text=f"Alert Threshold ({alert_threshold:.0%})",
    annotation_position="bottom right"
)

# Shade alert zones
for i, (date, occ) in enumerate(zip(forecast_df['week'], forecast_df['occupancy_rate'])):
    if occ < alert_threshold:
        fig.add_vrect(
            x0=date - pd.Timedelta(days=3),
            x1=date + pd.Timedelta(days=3),
            fillcolor="rgba(224, 90, 90, 0.1)",
            layer="below",
            line_width=0
        )

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E8E8E0'),
    height=420,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation='h', yanchor='bottom', y=1.02)
)

st.plotly_chart(fig, use_container_width=True)

# ── Forecast Table ────────────────────────────────────────────────────────────
st.subheader("📋 Weekly Forecast Breakdown")
forecast_display = forecast_df.copy()
forecast_display['week'] = forecast_display['week'].dt.strftime('%b %d, %Y')
forecast_display['occupancy_rate'] = forecast_display['occupancy_rate'].apply(lambda x: f"{x:.1%}")
forecast_display['status'] = forecast_df['occupancy_rate'].apply(
    lambda x: "🔴 Alert" if x < alert_threshold else "🟢 On Target"
)
forecast_display.columns = ['Week', 'Predicted Occupancy', 'Type', 'Status']
st.dataframe(forecast_display[['Week', 'Predicted Occupancy', 'Status']], use_container_width=True)

# ── LLM Marketing Alerts ──────────────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Marketing Intelligence")

alert_weeks = [(date, occ) for date, occ in zip(forecast_dates, forecasts) if occ < alert_threshold]

if not alert_weeks:
    st.success(f"✅ All {forecast_weeks} forecasted weeks are above the {alert_threshold:.0%} threshold. No alerts triggered.")
else:
    st.warning(f"⚠️ {len(alert_weeks)} week(s) forecasted below threshold. Generating marketing responses...")

    for date, occ in alert_weeks:
        week_label = date.strftime('%B %d, %Y')
        st.markdown(f"#### 📅 Week of {week_label} — Predicted: {occ:.1%}")

        with st.spinner(f"Generating marketing strategy for {week_label}..."):
            result = generate_marketing_alert(occ, week_label, hotel_type, alert_threshold)

        if result.get("triggered") and not result.get("error"):
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**📱 WhatsApp Message**")
                st.info(result.get("whatsapp_message", "N/A"))

                st.markdown("**📧 Email Subject**")
                st.info(result.get("email_subject", "N/A"))

            with col_b:
                st.markdown("**📸 Instagram Caption**")
                st.info(result.get("instagram_caption", "N/A"))

                st.markdown("**🎯 Strategy**")
                st.markdown(f"- **Recommended Offer:** {result.get('recommended_discount', 'N/A')}")
                st.markdown(f"- **Target Segment:** {result.get('target_segment', 'N/A')}")
        else:
            st.error(f"Agent error: {result.get('error', 'Unknown')}")

        st.divider()

# ── Feature Importance ────────────────────────────────────────────────────────
if model:
    st.subheader("🔍 What's Driving the Forecast")
    importance_df = pd.DataFrame({
        'feature': get_feature_columns(),
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=True)

    fig_imp = px.bar(
        importance_df, x='importance', y='feature',
        orientation='h',
        color='importance',
        color_continuous_scale='Viridis',
        template='plotly_dark'
    )
    fig_imp.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_imp, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("HotelPulse · Built with XGBoost + Prophet + Claude AI · Tracked with MLflow")
```

---

### ⏱ HOUR 4 (3:00–4:00) — Docker + Deploy on Render

#### Step 4.1 — Dockerfile (15 min)

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p data/raw data/processed artifacts mlruns

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run pipeline first, then dashboard
CMD ["sh", "-c", "python src/pipeline/run_pipeline.py && streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0"]
```

#### Step 4.2 — render.yaml (10 min)

```yaml
services:
  - type: web
    name: hotelpulse
    runtime: docker
    plan: free
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false          # you'll paste this in Render dashboard
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: ALERT_THRESHOLD
        value: "0.65"
    healthCheckPath: /_stcore/health
```

#### Step 4.3 — GitHub Actions CI (10 min)

`.github/workflows/deploy.yml`:
```yaml
name: Test & Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Deploy
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}
```

#### Step 4.4 — Deploy to Render (25 min)

```
1. Push everything to GitHub (main branch)
2. Go to render.com → New → Web Service
3. Connect your GitHub repo
4. Runtime: Docker (auto-detected from Dockerfile)
5. Add environment variables:
   - ANTHROPIC_API_KEY → paste your key
   - OPENWEATHER_API_KEY → paste your key
   - ALERT_THRESHOLD → 0.65
6. Click Deploy
7. Wait ~5 min for first build
8. Get your public URL: https://hotelpulse.onrender.com
```

**IMPORTANT:** Free Render tier requires you to copy `hotel_bookings.csv` into the Docker image (put it in `data/raw/` before pushing). The file is 8MB — fine for GitHub.

---

## 📋 COMPLETE CHECKLIST

### Before You Write One Line of Code
- [ ] Download Kaggle dataset → `data/raw/hotel_bookings.csv`
- [ ] Create UAE events CSV → `data/raw/events_calendar.csv`
- [ ] Get OpenWeatherMap API key → add to `.env`
- [ ] Get Anthropic API key → add to `.env`
- [ ] Create Render account (link GitHub)

### During Build
- [ ] Hour 1: Data loader + feature engineering working
- [ ] Run `python src/pipeline/run_pipeline.py` successfully
- [ ] MLflow UI shows a run at `localhost:5000`
- [ ] Hour 2: Model trains, saves to `artifacts/model.pkl`
- [ ] Hour 3: LLM agent returns marketing JSON
- [ ] Streamlit runs locally at `localhost:8501`
- [ ] Hour 4: Docker builds locally (`docker build -t hotelpulse .`)
- [ ] Docker runs locally (`docker run -p 8501:8501 hotelpulse`)

### Deployment
- [ ] Push to GitHub (include `data/raw/hotel_bookings.csv`)
- [ ] Create `render.yaml` in repo root
- [ ] Connect Render to GitHub repo
- [ ] Add env vars in Render dashboard
- [ ] First deploy succeeds
- [ ] Public URL works
- [ ] Add URL to resume + LinkedIn

---

## 🎯 What to Say in the Interview

> *"HotelPulse is a demand forecasting system I built to predict weekly hotel occupancy and automatically trigger LLM-generated marketing campaigns when demand is forecast to dip. It ingests hotel booking data alongside UAE event signals, engineers time-series features, and trains an XGBoost model tracked via MLflow. When predicted occupancy drops below a configurable threshold, a Claude-powered agent generates platform-specific marketing copy — WhatsApp messages, email subject lines, and Instagram captions — tailored to the property type. It's deployed live on Render."*

That's 30 seconds. Every sentence maps to a FIVE KPI.

---

## 📊 Resume Bullet Points (Copy-Paste Ready)

```
• Built HotelPulse, a production ML system forecasting weekly hotel occupancy demand 
  using XGBoost + Prophet on 119k booking records with engineered time-series features 
  (lag occupancy, UAE event signals, ADR trends); tracked experiments via MLflow

• Deployed an LLM marketing agent (Claude API) that automatically generates 
  platform-specific campaign copy (WhatsApp, email, Instagram) when forecasted 
  occupancy drops below threshold — directly reducing manual marketing response time

• Containerized and deployed full pipeline on Render with Docker; live at [URL]
```

---

*Total estimated time: 4 hours vibe-coding | Stack: Python, XGBoost, Prophet, MLflow, Streamlit, Claude API, Docker, Render*