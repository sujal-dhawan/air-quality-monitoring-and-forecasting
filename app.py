import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetch import fetch_air_quality_data_waqi
from forecast import forecast_aqi

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("Real-Time Air Quality Monitoring and Forecasting Dashboard")
st.markdown("""
This dashboard fetches real-time air quality data and forecasts future pollutant levels.
""")

# Sidebar configuration
st.sidebar.header("Configuration")
city = st.sidebar.text_input("City", "Noida").strip().lower()
parameter = st.sidebar.selectbox("Pollutant Parameter", ["pm25", "pm10", "o3", "no2", "so2", "co"])

st.sidebar.header("Forecast Settings")
periods = st.sidebar.number_input("Forecast Hours", value=24, min_value=1, step=1)

# Fetch data section
st.subheader("Current Air Quality Data")
with st.spinner("Fetching data..."):
    df = fetch_air_quality_data_waqi(city=city, parameter=parameter)

    # Data validation checks
    if df.empty or df['value'].isna().all():
        st.error("No valid data available. Please try a different city or parameter.")
        st.stop()

    # Data formatting
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.dropna(subset=['datetime', 'value'], inplace=True)

# Display raw data details
st.write(f"Available data points: {len(df)}")
st.write("Latest measurements:", df.tail())

# Plot current data
if not df.empty:
    fig = px.line(
        df,
        x="datetime",
        y="value",
        title=f"{parameter.upper()} Levels in {city.title()}",
        markers=True,
        line_shape="spline"
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=f"{parameter.upper()} Value",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data available to plot")

# Forecasting section
st.subheader("AQI Forecasting")
if st.button("Generate Forecast"):
    if len(df) < 10:  # More flexible minimum data requirement
        st.warning("Forecast may be less accurate with limited historical data")

    with st.spinner("Generating forecast..."):
        try:
            forecast, model = forecast_aqi(df, periods)

            # Plot forecast components
            st.write("Forecast Components")
            fig_components = model.plot_components(forecast)
            st.pyplot(fig_components)

            # Plot forecast with uncertainty intervals
            st.write("Forecast Results")
            fig_forecast = px.line(
                forecast,
                x="ds",
                y="yhat",
                title=f"{parameter.upper()} Forecast with Uncertainty",
                labels={"ds": "Date", "yhat": "Predicted Value"},
                line_shape="spline"
            )
            fig_forecast.add_scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                mode='lines',
                line=dict(color='gray', width=0.5),
                name='Upper Bound'
            )
            fig_forecast.add_scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                mode='lines',
                line=dict(color='gray', width=0.5),
                fill='tonexty',
                name='Lower Bound'
            )
            st.plotly_chart(fig_forecast, use_container_width=True)

            # Show forecast details
            forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
            forecast_display.columns = ["Date", "Predicted Value", "Lower Bound", "Upper Bound"]
            st.write("Forecast Data Summary", forecast_display)


        except Exception as e:
            st.error(f"Forecasting failed: {str(e)}")