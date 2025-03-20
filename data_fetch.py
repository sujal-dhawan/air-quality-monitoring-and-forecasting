import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

WAQI_API_TOKEN = "285f37fa7aee662f65aa5dca248ac7c439520865"


def fetch_air_quality_data_waqi(city="noida", parameter="pm25"):
    """
    Fetch air quality data with generated historical data for demonstration.
    Returns DataFrame with datetime and value columns.
    """
    # Fetch current data from WAQI API
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_TOKEN}"
    response = requests.get(url)

    df = pd.DataFrame(columns=["datetime", "value"])
    current_value = np.nan
    current_time = datetime.now()

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'ok':
            current_data = data.get('data', {})
            iaqi = current_data.get('iaqi', {})
            param_data = iaqi.get(parameter, {})
            current_value = param_data.get('v', np.nan)
            current_time = pd.to_datetime(current_data.get('time', {}).get('s', datetime.now()))

            # Generate synthetic historical data if current value is available
            if not np.isnan(current_value):
            # Create 24 hours of historical data with some variance
                historical_times = [current_time - timedelta(hours=i) for i in range(24, 0, -1)]
            np.random.seed(42)  # For reproducible dummy data
            historical_values = np.random.normal(current_value, 5, 24).clip(0)  # Prevent negative values

            # Create DataFrame with combined data
            df = pd.DataFrame({
                "datetime": historical_times + [current_time],
                "value": historical_values.tolist() + [current_value]
            })

            # Clean and format data
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df.dropna(subset=['value'], inplace=True)
            df.sort_values('datetime', inplace=True)
            df.reset_index(drop=True, inplace=True)

    return df