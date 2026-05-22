import logging
import requests
from google import genai
from google.genai import types

from app.config import get_settings

logger = logging.getLogger(__name__)


def _gemini_client():
    return genai.Client(api_key=get_settings().GOOGLE_API_KEY)


# ─── LOCAL EVENTS (SERP) ──────────────────────────────────────────────────────

def fetch_local_events(city: str) -> dict:
    """
    Fetches upcoming local events for *city* via SerpAPI Google Events engine.
    Returns raw JSON dict (or an error dict).
    """
    settings = get_settings()
    try:
        url = (
            f"https://serpapi.com/search.json"
            f"?engine=google_events&q=Events+in+{city}&api_key={settings.SERP_API_KEY}"
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.error("SerpAPI error: %s", exc)
        return {"error": str(exc)}


# ─── SMART DAY PLANNER ────────────────────────────────────────────────────────

def generate_day_plan(city: str) -> str:
    """
    Asks Gemini (with function-calling tools) to build a full personalised
    day itinerary for *city*, combining weather forecast, tourist spots,
    and local events.
    """
    client = _gemini_client()

    # ── Define tool functions that Gemini can call ────────────────────────
    def get_forecasted_weather(city: str) -> str:  # noqa: F811
        """
        Fetches the weather forecast and top tourist places for the given city using web search.

        Args:
            city: City name (e.g. Delhi, Dehradun)
        """
        import datetime
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool])
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                f"Provide the detailed weather forecast for {city} on {datetime.date.today()}. "
                f"Then also list the top recommended places to visit in {city} on the same date. "
                f"Format the response clearly so it can be used by another planning agent."
            ),
            config=config,
        )
        return resp.text

    def find_local_events(city: str) -> dict:  # noqa: F811
        """
        Finds local events for the given city using SerpAPI.

        Args:
            city: City name (e.g. Delhi, Mumbai)
        """
        return fetch_local_events(city)

    # ── Planner prompt ────────────────────────────────────────────────────
    prompt = f"""
You are a smart travel and event planner assistant.

Your job is to create a personalised day itinerary for the user in {city} without asking any questions.

Budget: Plan the whole day for an upper-middle-class user.

Your goal is to suggest the best itinerary that enhances knowledge, social engagement, and health,
along with fun, calm, and relaxing activities.

You are given:
- Weather forecast for {city} (temperature, rain chances, humidity, etc.) and a list of recommended
  places to visit on the same day. (Use the get_forecasted_weather function.)
- Upcoming events in {city} with title, date, time, venue, description, and link.
  (Use the find_local_events function.)

Instructions:
- Start with a warm, friendly greeting acknowledging the user and including the city name.
- Always use weather conditions to decide outdoor vs indoor activities.
- Include healthy activities in the early morning (e.g. skating, gym, park visits).
- Day starts early morning (7–8 AM) and can end around midnight (1–2 AM).
- Organise the plan chronologically (Morning → Afternoon → Evening) with timestamps.
- Do NOT mention any function names in the response.
- Mix tourist attractions + events + leisure breaks for a balanced day.
- Plan events across a wide range of interests (history, art, wildlife, food, tech, etc.).
- Act as a tour guide: explain the history, importance, benefits, and fun of each activity.
- Plan budget-friendly options; mention discount offers via event links when applicable.
- Check that event timing fits the user's schedule before including it.
- Always include event links when mentioning events.
- Suggest lunch/dinner breaks with local cuisine or mall recommendations.
- If multiple good options exist at the same time, present them as choices.
- Keep the tone friendly and actionable; add relevant emojis like a local guide.
- Do not end with questions asking for feedback or improvements.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[find_local_events, get_forecasted_weather]
        ),
    )

    # Extract first text part from response
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            return part.text

    return "Unable to generate itinerary. Please try again."
