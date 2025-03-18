# forecast.py
from prophet import Prophet
import pandas as pd


def forecast_aqi(df, periods=24):
    """
    Forecast future AQI values using Prophet.
    - df: DataFrame with 'datetime' and 'value' columns.
    - periods: Number of hours into the future to forecast.
    Returns the forecast DataFrame and the trained model.
    """
    # Ensure 'datetime' is in correct format and 'value' is numeric
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Drop NaN values
    df.dropna(subset=['datetime', 'value'], inplace=True)

    # Check if there are enough data points
    if df.shape[0] < 2:
        raise ValueError("Not enough valid data for forecasting. Try a different city or parameter.")

    # Prepare data for Prophet
    df_prophet = df.rename(columns={"datetime": "ds", "value": "y"})

    # Initialize and fit the model
    model = Prophet()
    model.fit(df_prophet)

    # Create a future DataFrame with hourly frequency
    future = model.make_future_dataframe(periods=periods, freq='H')
    forecast = model.predict(future)

    return forecast, model
