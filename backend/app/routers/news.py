from fastapi import APIRouter, HTTPException
from app.schemas import (
    NewsRequest,
    NewsResponse,
    ArticleSummaryRequest,
    ArticleSummaryResponse,
)
from app.services.news_service import fetch_news, summarize_article

router = APIRouter()


@router.post("/headlines", response_model=NewsResponse, summary="Fetch latest news headlines")
async def get_headlines(payload: NewsRequest):
    """
    Fetch the latest news headlines for a given topic from NewsAPI.
    Returns up to *page_size* articles (default 5, max 20).
    """
    try:
        articles = fetch_news(topic=payload.topic, page_size=payload.page_size)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return NewsResponse(topic=payload.topic, articles=articles)


@router.post("/summarize", response_model=ArticleSummaryResponse, summary="AI-summarise a news article")
async def summarize_news_article(payload: ArticleSummaryRequest):
    """
    Provide a news article URL and receive a clean 4–5 line Gemini summary.
    """
    try:
        summary = summarize_article(payload.url)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization error: {exc}")

    return ArticleSummaryResponse(url=payload.url, summary=summary)
