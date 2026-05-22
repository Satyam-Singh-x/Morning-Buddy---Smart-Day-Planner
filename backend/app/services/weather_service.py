import logging
import requests
from google import genai
from google.genai import types
import datetime

from app.config import get_settings
from app.schemas import WeatherData

logger = logging.getLogger(__name__)


def _gemini_client():
    return genai.Client(api_key=get_settings().GOOGLE_API_KEY)


# ─── CURRENT WEATHER ──────────────────────────────────────────────────────────

def fetch_current_weather(city: str) -> WeatherData:
    """
    Calls OpenWeather current-weather endpoint and returns a typed WeatherData object.
    Raises ValueError on API error.
    """
    settings = get_settings()
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    )
    resp = requests.get(url, timeout=10)
    data = resp.json()

    if resp.status_code != 200:
        raise ValueError(data.get("message", "OpenWeather API error"))

    return WeatherData(
        city=data["name"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        wind=data["wind"]["speed"],
        condition=data["weather"][0]["description"],
    )


# ─── GEMINI ANALYSIS ──────────────────────────────────────────────────────────

def analyze_weather(weather: WeatherData) -> str:
    """
    Sends structured weather data to Gemini and returns a friendly conversational analysis.
    """
    client = _gemini_client()
    prompt = f"""
You are a friendly weather assistant. First greet the user and provide the city name as a heading.

Weather data:
- City: {weather.city}
- Temperature: {weather.temperature}°C (feels like {weather.feels_like}°C)
- Humidity: {weather.humidity}%
- Wind Speed: {weather.wind} m/s
- Condition: {weather.condition}

Your task:
1. Give a short and friendly weather report.
2. Suggest what to wear or carry.
3. Keep it natural and conversational.
4. Do NOT mention APIs or JSON.
5. Keep it concise (4–6 lines).
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


# ─── FORECAST + PLACES (GROUNDED) ─────────────────────────────────────────────

def fetch_forecast_and_places(city: str) -> str:
    """
    Uses Gemini with Google Search grounding to get today's forecast
    and recommended tourist places for a city.
    """
    client = _gemini_client()
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    config = types.GenerateContentConfig(tools=[grounding_tool])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            f"Provide the detailed weather forecast for {city} on {datetime.date.today()}. "
            f"Then list the top recommended places to visit in {city} on the same date. "
            f"Format the response clearly so it can be used by a planning agent."
        ),
        config=config,
    )
    return response.text
