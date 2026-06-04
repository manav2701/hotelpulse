import requests, os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

def fetch_weather_signal(city: str = "Dubai", days_back: int = 90) -> dict:
    """Fetch historical avg temperature as demand proxy."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    # Use current weather as a stand-in signal for demo
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {"temp": data['main']['temp'], "condition": data['weather'][0]['main']}
    except requests.RequestException:
        pass
    return {"temp": 28.0, "condition": "Clear"}  # fallback for demo
