# EgyptAir SkyCast

## Project Overview

This project builds a data pipeline that fetches EgyptAir flight data using the AviationStack API and scrapes weather information from [Weather-Forecast.com](https://www.weather-forecast.com/). I essentially did this project for myself, as I travel a lot on EgyptAir and I find myself always interested in knowing what the weather will be like once I arrive to my destination country. Therefore, I believe that this combined dataset provides valuable insights by merging flight details with the weather conditions at the arrival cities. Above all, this dataset is not publicly available for free and offers real-world value for analysis, forecasting, and decision-making in the aviation industry.

## Data Sources

1. **AviationStack API**
   - **Purpose:** To retrieve real-time flight data for EgyptAir.
   - **Endpoint:** `http://api.aviationstack.com/v1/flights`
   - **API Key:** `4ae459e6fe4e65e9e367a95cc25dddad`

2. **Weather-Forecast.com**
   - **Purpose:** To scrape weather temperature data for arrival cities.
   - **URL Pattern:** `https://www.weather-forecast.com/locations/{city}/forecasts/latest`

## Dataset Description

The final dataset includes the following fields:

- **Flight Number**
- **Departure Airport**
- **Arrival Airport**
- **Flight Status**
- **Scheduled Departure**
- **Scheduled Arrival**
- **Arrival Timezone**
- **Temperature °C**

This dataset allows users to analyze flight schedules alongside weather conditions, enabling better planning and forecasting.

## Value Proposition

- **Unique Insights:** Combines flight data with weather conditions, which is not readily available in a single dataset.
- **Decision Making:** Helps in understanding the impact of weather on flight schedules and statuses.
- **Time-Saving:** Automates the process of data collection from multiple sources, ensuring up-to-date information.

# Getting Started

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/khat3r/SkyCast.git
   cd SkyCast
   
      ```
2. **Set Up a Virtual Environment**

    python -m venv venv
    source venv/bin/activate
    
3. **Install Required Packages**
    
    pip install -r requirements.txt

4. **Run the Script**

    python main.py

The script will fetch flight data, scrape weather information, and save the combined dataset to egyptair_flights_with_weather.csv.

