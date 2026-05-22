import logging
import requests
from google import genai
from typing import List

from app.config import get_settings
from app.schemas import ArticleItem

logger = logging.getLogger(__name__)


def _gemini_client():
    return genai.Client(api_key=get_settings().GOOGLE_API_KEY)


# ─── FETCH HEADLINES ──────────────────────────────────────────────────────────

def fetch_news(topic: str, page_size: int = 5) -> List[ArticleItem]:
    """
    Fetches latest articles for *topic* from NewsAPI.
    Raises ValueError on API-level errors.
    """
    settings = get_settings()
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={topic}&pageSize={page_size}&sortBy=publishedAt&apiKey={settings.NEWS_API_KEY}"
    )
    resp = requests.get(url, timeout=10)
    data = resp.json()

    if resp.status_code != 200:
        raise ValueError(data.get("message", "NewsAPI error"))

    raw_articles = data.get("articles", [])
    return [ArticleItem(**a) for a in raw_articles]


# ─── SUMMARISE ONE ARTICLE ────────────────────────────────────────────────────

def summarize_article(url: str) -> str:
    """
    Asks Gemini to summarise a news article at *url* in 4–5 lines.
    """
    client = _gemini_client()
    prompt = f"""
Summarize this news article clearly in 4–5 lines.
Do not mention the source, article name, or URL.
Keep it clean and informative.

URL: {url}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
