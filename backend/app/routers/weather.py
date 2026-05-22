from fastapi import APIRouter, HTTPException
from app.schemas import (
    WeatherRequest,
    WeatherAnalysisResponse,
    WeatherForecastRequest,
    WeatherForecastResponse,
)
from app.services.weather_service import (
    fetch_current_weather,
    analyze_weather,
    fetch_forecast_and_places,
)

router = APIRouter()


@router.post("/current", response_model=WeatherAnalysisResponse, summary="Current weather + AI analysis")
async def current_weather(payload: WeatherRequest):
    """
    Fetch real-time weather for a city and return a Gemini-powered
    friendly analysis with clothing/travel advice.
    """
    try:
        weather_data = fetch_current_weather(payload.city)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    analysis = analyze_weather(weather_data)

    return WeatherAnalysisResponse(weather=weather_data, analysis=analysis)


@router.post("/forecast", response_model=WeatherForecastResponse, summary="Forecast + tourist places (grounded AI)")
async def weather_forecast(payload: WeatherForecastRequest):
    """
    Uses Gemini with Google Search grounding to return today's detailed
    weather forecast AND top places to visit for the city.
    """
    try:
        forecast_text = fetch_forecast_and_places(payload.city)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Forecast error: {exc}")

    return WeatherForecastResponse(city=payload.city, forecast=forecast_text)
