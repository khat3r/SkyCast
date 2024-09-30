import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession

#constants
AVIATIONSTACK_API_KEY = "4ae459e6fe4e65e9e367a95cc25dddad"
AVIATIONSTACK_URL = f"http://api.aviationstack.com/v1/flights?access_key={AVIATIONSTACK_API_KEY}&airline_iata=MS"
WEATHER_BASE_URL = "https://www.weather-forecast.com/locations/{}/forecasts/latest"

#function to scrape temperature from Weather-forecast.com
def scrape_weather_temperature_forecast_com(city):
    if city == "N/A" or not city:
        return "N/A"

    #replace spaces with hyphens for url
    city_formatted = city.replace(' ', '-')
    url = WEATHER_BASE_URL.format(city_formatted)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/94.0.4606.81 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching temperature for {city}: {e}")
        return "N/A"

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        #extract temperature
        temp_section = soup.find("span", class_="temp b-forecast__table-value")
        temperature = temp_section.get_text().strip() if temp_section else "N/A"
        return temperature
    except AttributeError:
        print(f"Could not find temperature on the page for {city}.")
        return "N/A"


#function to clean and organize the flight and weather data
def clean_and_process_data(flight_data):
    flights = []

    for flight in flight_data:
        # Use .get to avoid Keyerror and return 'N/A' if key's missing
        dep_airport = flight['departure'].get('airport', 'N/A')
        arr_airport = flight['arrival'].get('airport', 'N/A')
        dep_time = flight['departure'].get('scheduled', 'N/A')
        arr_time = flight['arrival'].get('scheduled', 'N/A')
        arr_timezone = flight['arrival'].get('timezone', 'N/A')
        flight_status = flight.get('flight_status', 'N/A')
        flight_number = flight.get('flight', {}).get('iata', 'N/A')

        #extract arrival city from timezone
        if arr_timezone != "N/A" and '/' in arr_timezone:
            arrival_city = arr_timezone.split('/')[-1].replace('_', ' ')
        else:
            arrival_city = "N/A"

        #get weather for arrival city
        temperature = scrape_weather_temperature_forecast_com(arrival_city)
        if temperature == "N/A":
            print(f"Retrying to fetch again for {arrival_city}...")
            temperature = scrape_weather_temperature_forecast_com(arrival_city+"-city")
            if temperature == "N/A":
                print(f"Couldn't find {arrival_city} city on weather-forecast.com")
            else:
                print(f"Successfully retrieved the temperature for {arrival_city}\n")

        #append flight data with weather information
        flights.append({
            "Flight Number": flight_number,
            "Departure Airport": dep_airport,
            "Arrival Airport": arr_airport,
            "Flight Status": flight_status,
            "Scheduled Departure": dep_time,
            "Scheduled Arrival": arr_time,
            "Arrival Timezone": arr_timezone,
            "Temperature °C": temperature
        })

    #create a data frame to organize data
    df_flights = pd.DataFrame(flights)
    return df_flights

#function to save dataset to CSV
def save_dataset(df, filename="egyptair_flights_with_weather.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename}")
    except Exception as e:
        print(f"Error saving dataset: {e}")

#fetching flight data from the AviationStack API
def fetch_egyptair_flight_data():
    try:
        response = requests.get(AVIATIONSTACK_URL)
        response.raise_for_status()  # Check for errors
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from AviationStack API: {e}")
        return []

#our main
def main():
    print("Fetching EgyptAir flight data from API..")
    flight_data = fetch_egyptair_flight_data()

    if flight_data:
        print("Processing flight and weather data..")
        final_dataset = clean_and_process_data(flight_data)

        print("Saving dataset..")
        save_dataset(final_dataset)

        print("Data pipeline completed successfully!")
    else:
        print("No flight data available to process.")

if __name__ == "__main__":
    main()
