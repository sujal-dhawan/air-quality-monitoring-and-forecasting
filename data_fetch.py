import requests
import pandas as pd
from datetime import datetime

# WAQI API Token (Sign up at https://aqicn.org/data-platform/token/)
WAQI_API_TOKEN = "285f37fa7aee662f65aa5dca248ac7c439520865"  # Replace with your WAQI API token


def fetch_air_quality_data_waqi(city="noida", parameter="pm25"):
    """
    Fetch air quality data from the WAQI API for a given city and pollutant parameter.
    Returns a DataFrame with datetime and value columns.
    """
    # WAQI API endpoint for city feed
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_TOKEN}"

    # Make the API request
    response = requests.get(url)

    # Debugging: Print API response
    print("WAQI API URL:", url)
    print("WAQI API Response Status Code:", response.status_code)
    print("WAQI API Response Data:", response.json())

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            # Extract relevant data
            measurements = []
            iaqi = data['data']['iaqi']  # Individual Air Quality Index (IAQI) data
            for key, value in iaqi.items():
                if parameter == key:  # Filter for the specified parameter (e.g., pm25)
                    measurements.append({
                        "datetime": data['data']['time']['s'],  # Timestamp of the measurement
                        "value": value['v']  # Value of the pollutant
                    })
            # Create a DataFrame
            df = pd.DataFrame(measurements)
            # Convert datetime to a proper format
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.sort_values("datetime", inplace=True)
            df.reset_index(drop=True, inplace=True)
            return df
    else:
        print("Error fetching data from WAQI API. Status Code:", response.status_code, response.text)

    # Return an empty DataFrame if no data is found
    return pd.DataFrame()