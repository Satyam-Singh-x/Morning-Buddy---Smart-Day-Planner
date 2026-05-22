from fastapi import APIRouter, HTTPException
from app.schemas import PlannerRequest, PlannerResponse
from app.services.planner_service import generate_day_plan

router = APIRouter()


@router.post("/generate", response_model=PlannerResponse, summary="Generate a personalised full-day itinerary")
async def smart_plan(payload: PlannerRequest):
    """
    Generates a complete personalised day itinerary for a city.

    Internally Gemini calls:
    - `get_forecasted_weather` → today's weather + tourist spots (grounded via Google Search)
    - `find_local_events`      → upcoming local events via SerpAPI

    Returns a markdown-formatted plan with timestamps, event links, food suggestions, and tips.
    """
    try:
        itinerary = generate_day_plan(payload.city)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Planner error: {exc}")

    return PlannerResponse(city=payload.city, itinerary=itinerary)
