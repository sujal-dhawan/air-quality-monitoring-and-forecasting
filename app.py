import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetch import fetch_air_quality_data_waqi
from forecast import forecast_aqi

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("Real-Time Air Quality Monitoring and Forecasting Dashboard")
st.markdown("""
This dashboard fetches real-time air quality data from the WAQI API and uses Prophet to forecast future pollutant levels.
""")

# Sidebar for user inputs
st.sidebar.header("Configuration")
city = st.sidebar.text_input("City", "Noida")
parameter = st.sidebar.selectbox("Pollutant Parameter", ["pm25", "pm10", "o3", "no2", "so2", "co"])

st.sidebar.header("Forecast Settings")
periods = st.sidebar.number_input("Forecast Hours", value=24, min_value=1, step=1)

# Fetch data
st.subheader("Current Air Quality Data")
with st.spinner("Fetching data..."):
    df = fetch_air_quality_data_waqi(city=city, parameter=parameter)

    # Debug: Inspect DataFrame
    st.write("DataFrame Head:", df.head())
    st.write("DataFrame Info:", df.info())
    st.write("Number of Non-NaN Rows:", df.dropna().shape[0])

if df.empty:
    st.error("No data available. Please try again later or adjust your parameters.")
else:
    # Ensure 'datetime' and 'value' columns are in the correct format
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(inplace=True)

    st.write("Latest data records:", df.tail())

    # Plot current air quality time series with markers
    if not df.empty:
        fig = px.line(
            df,
            x="datetime",
            y="value",
            title=f"{parameter.upper()} Levels in {city}",
            markers=True,  # Enable markers for better visibility
            line_shape="spline"  # Make lines smooth
        )
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title=f"{parameter.upper()} Value",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No valid data available to plot.")

    # Forecasting section
    st.subheader("Forecast Future AQI Levels")
    if st.button("Run Forecast"):
        if df.shape[0] < 2:
            st.error("Not enough data available for forecasting. Please fetch more data.")
        else:
            with st.spinner("Running forecast..."):
                forecast, model = forecast_aqi(df, periods)
                st.write("Forecasted Data (last 5 records):", forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

                # Plot forecasted values with markers
                fig_forecast = px.line(
                    forecast,
                    x="ds",
                    y="yhat",
                    title="Forecasted AQI Levels",
                    markers=True,  # Enable markers for better visibility
                    line_shape="spline"
                )
                st.plotly_chart(fig_forecast, use_container_width=True)
                st