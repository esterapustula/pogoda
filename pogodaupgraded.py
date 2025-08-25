import requests
import datetime
import json
import os

class WeatherForecast:
    API_URL = "https://api.open-meteo.com/v1/forecast"
    LAT, LON = 54.3520, 18.6466
    CACHE_FILE = "pogoda.json"

    def __init__(self):
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _fetch_weather(self, date: str) -> str:
        url = (
            f"{self.API_URL}?latitude={self.LAT}&longitude={self.LON}"
            f"&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            return "Nie wiem"

        data = response.json()
        daily = data.get("daily")
        if not daily:
            return "Nie wiem"

        rain_values = daily.get("rain_sum")
        if not rain_values or not isinstance(rain_values, list):
            return "Nie wiem"

        rain = rain_values[0]
        if rain is None or rain < 0:
            return "Nie wiem"
        elif rain == 0:
            return "Nie będzie padać"
        return "Będzie padać"


    def __getitem__(self, date: str) -> str:
        if date not in self.cache:
            self.cache[date] = self._fetch_weather(date)
            self._save_cache()
        return self.cache[date]

    def __setitem__(self, date: str, forecast: str):
        self.cache[date] = forecast
        self._save_cache()

    def __iter__(self):
        return iter(self.cache.keys())

    def items(self):
        return self.cache.items()

if __name__ == "__main__":
    weather_forecast = WeatherForecast()

    d = input("Podaj datę w formacie YYYY-MM-DD lub ENTER dla jutra: ").strip()
    if not d:
        d = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"{d}: {weather_forecast[d]}")

    print("\nZapisane prognozy:")
    for date, forecast in weather_forecast.items():
        print(f"{date}: {forecast}")