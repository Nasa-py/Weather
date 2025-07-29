import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")
url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if data["cod"] == 200:
    main = data["main"]
    weather = data["weather"][0]
    print(f"\nWeather in {city}:")
    print(f"Temperature: {main['temp']}°C")
    print(f"Humidity: {main['humidity']}%")
    print(f"Condition: {weather['description'].title()}")
else:
    print("City not found 😢")
