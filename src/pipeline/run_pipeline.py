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
