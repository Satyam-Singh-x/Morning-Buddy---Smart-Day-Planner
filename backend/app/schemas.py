from pydantic import BaseModel, Field
from typing import Optional, List


# ─── WEATHER ──────────────────────────────────────────────────────────────────

class WeatherRequest(BaseModel):
    city: str = Field(..., example="Kolkata", description="City name to fetch weather for")

class WeatherData(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    wind: float
    condition: str

class WeatherAnalysisResponse(BaseModel):
    weather: WeatherData
    analysis: str           # Gemini-generated friendly report
    narrate: bool = False   # client sets this to request audio from /api/tts

class WeatherForecastRequest(BaseModel):
    city: str = Field(..., example="Delhi")

class WeatherForecastResponse(BaseModel):
    city: str
    forecast: str           # Gemini grounded forecast + places text


# ─── NEWS ─────────────────────────────────────────────────────────────────────

class NewsRequest(BaseModel):
    topic: str = Field(..., example="artificial intelligence")
    page_size: int = Field(default=5, ge=1, le=20)

class ArticleSummaryRequest(BaseModel):
    url: str = Field(..., example="https://example.com/article")

class ArticleItem(BaseModel):
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    publishedAt: Optional[str]
    source: Optional[dict]

class NewsResponse(BaseModel):
    topic: str
    articles: List[ArticleItem]

class ArticleSummaryResponse(BaseModel):
    url: str
    summary: str


# ─── PLANNER ──────────────────────────────────────────────────────────────────

class PlannerRequest(BaseModel):
    city: str = Field(..., example="Mumbai", description="City for which to generate the day plan")

class PlannerResponse(BaseModel):
    city: str
    itinerary: str          # Full Gemini-generated day plan markdown text


# ─── TTS ──────────────────────────────────────────────────────────────────────

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    lang: str = Field(default="en", description="Language code, e.g. 'en', 'hi'")
    slow: bool = Field(default=False)
