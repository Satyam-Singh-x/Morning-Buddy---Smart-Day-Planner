from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import weather, news, planner, tts
import uvicorn

app = FastAPI(
    title="Udaya AI – Morning Buddy API",
    description="Smart AI-powered morning companion backend: weather, news, planning, and voice narration.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ──────────────────────────────────────────────────────────────────────
# Allow your React frontend origin(s). Adjust in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ──────────────────────────────────────────────────────────────────
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(news.router,    prefix="/api/news",    tags=["News"])
app.include_router(planner.router, prefix="/api/planner", tags=["Smart Planner"])
app.include_router(tts.router,     prefix="/api/tts",     tags=["Text-to-Speech"])


# ─── HEALTH ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Udaya AI backend is running 🌅"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
