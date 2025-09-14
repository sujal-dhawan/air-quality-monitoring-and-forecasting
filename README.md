# Air Quality Monitoring & Forecasting Dashboard ☁️📈

A user-friendly web application built with Streamlit and Python to monitor real-time air quality data and forecast future trends using machine learning.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://air-quality-monitoring-and-forecasting.streamlit.app/)

## Overview

This dashboard provides a seamless interface to visualize current and historical air quality for any city. It leverages the WAQI (World Air Quality Index) API for live data and uses the powerful Facebook Prophet library to generate accurate time-series forecasts, helping users understand potential air pollution trends.


## Key Features ✨

* **Real-Time Data:** Fetches live air quality data for 6 major pollutants (PM2.5, PM10, O₃, NO₂, SO₂, CO).
* **Interactive UI:** Allows users to easily select any city and pollutant parameter.
* **Time-Series Forecasting:** Utilizes Facebook Prophet to predict future air quality levels with a user-defined forecast period.
* **Rich Visualizations:** Employs Plotly to create interactive charts for both current data and forecast results, including uncertainty intervals.
* **Synthetic Data Generation:** A unique feature that creates a plausible 24-hour historical dataset from a single real-time data point, ensuring the forecasting model can run reliably.
* **Modular Code:** The project is structured with separate modules for data fetching, forecasting, and the main app for better readability and maintenance.

## Technology Stack 🛠️

* **Language:** Python
* **Web Framework:** Streamlit
* **Machine Learning:** Prophet
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly
* **API Interaction:** Requests
* **Deployment:** Streamlit Cloud

## How to Run Locally 🚀

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Python 3.8+
* pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```
2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

The application should now be open and running in your web browser!

## Project Structure 📂

.
├── app.py              # Main Streamlit application file
├── data_fetch.py       # Module for fetching data from WAQI API
├── forecast.py         # Module for time-series forecasting with Prophet
├── requirements.txt    # List of project dependencies
└── README.md           # Project documentation
