import requests # Import request module (Need to install if not already)
import os
from datetime import datetime

def get_coordinates(city): # Take city as argumant.
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json" # Api request for latitude and longitude from open mateo
    response = requests.get(geocode_url) # Request api
    data = response.json() # Convert the response to JSON
    
    if 'results' in data and len(data['results']) > 0: # Check if the response is valid
        coordinates = data['results'][0] # Get the first result
        latitude = coordinates['latitude'] # Get the latitude from the json
        longitude = coordinates['longitude'] # Get the longitude
        return latitude, longitude # Return them
    else: # If not valid, return none
        return None, None
    
def create_directories(base_dir): # Function to store the weather reports
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Get the current time
    report_dir = os.path.join(base_dir, current_time) # Create a directory for every report based on the time
    suffix = 1 # A suffix so names don't mixed up
    
    while os.path.exists(report_dir):
        report_dir = os.path.join(base_dir, f"{current_time}_{suffix}")
        suffix += 1

    os.makedirs(report_dir)
    return report_dir

def generate_qr_code(text, report_dir):
    qr_code_url = "https://api.qrserver.com/v1/create-qr-code/?size=550x550&data=" + text + "&format=svg"
    response = requests.get(qr_code_url)
    qr_code_image = response.content
    qr_code_file = os.path.join(report_dir, "weather_report_qr.svg")
    with open(qr_code_file, 'wb') as file:
        file.write(qr_code_image)
    return qr_code_image


def get_weather(latitude, longitude): # Take latitude and longitue as argumant
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,precipitation,visibility,relative_humidity_2m,cloudcover,pressure_msl,dewpoint_2m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset&hourly=temperature_2m&timezone=auto" # API request URL
    response = requests.get(weather_url) # Request based on the latitude and longitude
    weather_data = response.json() # Convert to json
    return weather_data # Return it.

def generate_report(city):
    latitude, longitude = get_coordinates(city) # Get longitude and lattude
    print(f"Latutude: {latitude} \nLongitude: {longitude}\n")
    if latitude is None or longitude is None: 
        return "Couldn't find the location. Please check the city name and try again." 

    weather = get_weather(latitude, longitude) 
    if weather is None: 
        return "Failed to retrieve weather data. Please try again later."

    
    
    if latitude and longitude: # Complete the tasks if the locations exists
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        weather = get_weather(latitude, longitude) # Then get the weather
        # Get details from the weather data
        current_weather = weather.get('current', {})
        temperature = current_weather.get('temperature_2m', 'N/A') # Get current temperature
        wind_speed = current_weather.get('wind_speed_10m', 'N/A') # Get current wind speed
        humidity = current_weather.get('relative_humidity_2m', 'N/A') # Get current humidity
        precipitation = current_weather.get('precipitation', 'N/A') # Get precipitation
        visibility = current_weather.get('visibility', 'N/A')
        cloudcover = current_weather.get('cloudcover', 'N/A') # Get cloud cover
        pressure = current_weather.get('pressure_msl', 'N/A') # Get pressure at sea level
        dewpoint = current_weather.get('dewpoint_2m', 'N/A') # Get dew point

        # Get daily weather details
        daily_weather = weather.get('daily', {})
        temp_max = daily_weather.get('temperature_2m_max', ['N/A'])[0] # Max daily temperature
        temp_min = daily_weather.get('temperature_2m_min', ['N/A'])[0] # Min daily temperature
        daily_precipitation = daily_weather.get('precipitation_sum', ['N/A'])[0]
        sunrise = daily_weather.get('sunrise', ['N/A'])[0] # Sunrise time
        sunset = daily_weather.get('sunset', ['N/A'])[0] # Sunset time


        # Get units from the weather data
        ucurrent_weather = weather.get('current_units', {})
        utemperature = ucurrent_weather.get('temperature_2m', 'N/A') # Get current temperature unit
        uwind_speed = ucurrent_weather.get('wind_speed_10m', 'N/A') # Get current wind speed unit
        uhumidity = ucurrent_weather.get('relative_humidity_2m', 'N/A') # Get current humidity unit
        uprecipitation = ucurrent_weather.get('precipitation', 'N/A') # Get precipitation unit
        uvisibility = ucurrent_weather.get('visibility', 'N/A') # Get visibility
        ucloudcover = ucurrent_weather.get('cloudcover', 'N/A') # Get cloud cover unit
        upressure = ucurrent_weather.get('pressure_msl', 'N/A') # Get pressure unit
        udepoint = ucurrent_weather.get('dewpoint_2m', 'N/A') # Get dew point unit

        # Print the weather details
        report = (f"Report generated at {current_time}\n\n"
                  f"Latitude: {latitude}\n"
                  f"Lonitude: {longitude}\n\n"
                  f"Current temperature in {city} is {temperature}{utemperature}\n"
                  f"Wind speed is {wind_speed} {uwind_speed}\n"
                  f"Humidity is {humidity}{uhumidity}\n"
                  f"Precipitation is {precipitation} {uprecipitation}\n"
                  f"Visibility is {visibility}{uvisibility}\n"
                  f"Cloud cover is {cloudcover}{ucloudcover}\n"
                  f"Pressure is {pressure}{upressure}\n"
                  f"Dew point is {dewpoint}{udepoint}\n"
                  f"Max temperature today is {temp_max}{utemperature}\n"
                  f"Min temperature today is {temp_min}{utemperature}\n"
                  f"Daily precipitation is {daily_precipitation}{uprecipitation}\n"
                  f"Sunrise at {sunrise}\n"
                  f"Sunset at {sunset}")


        # Create directories and write report to a file
        base_dir = "Weather_reports_Python"
        report_dir = create_directories(base_dir) # Create directory if doesn't exists
        report_file = os.path.join(report_dir, "report.txt") # Add the file in the path

        with open(report_file, 'w') as file: 
            file.write(report) # Open the file and write report in it.

        # Generate QR code
        qr_code_image = generate_qr_code(report, report_dir)
        return report, qr_code_image # Return the report

    else: # Return error messege if the location is invalid
        return "Couldn't find the location. Please check the city name and try again. And check your internet connection."
def main(city):
    return generate_report(city)

# print(main("dhaka"))