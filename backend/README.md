# 🌅 Udaya AI – FastAPI Backend

Smart morning companion backend with weather, news, planning, and voice narration.

## Quick Start

```bash
# 1. Clone & enter directory
cd udaya-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your real API keys

# 5. Run the server
uvicorn app.main:app --reload
```

Server starts at **http://localhost:8000**

Interactive docs: **http://localhost:8000/docs**

---

## API Endpoints

### 🌤 Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/weather/current` | Real-time weather + Gemini analysis |
| POST | `/api/weather/forecast` | Today's forecast + tourist spots (grounded AI) |

### 📰 News
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/news/headlines` | Latest headlines by topic (NewsAPI) |
| POST | `/api/news/summarize` | AI summary of a news article URL |

### 🧠 Smart Planner
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/planner/generate` | Full personalized day itinerary |

### 🔊 Text-to-Speech
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tts/speak` | Streams MP3 audio from text |

---

## Example Requests

### Current Weather
```json
POST /api/weather/current
{
  "city": "Kolkata"
}
```

### News Headlines
```json
POST /api/news/headlines
{
  "topic": "technology",
  "page_size": 5
}
```

### Article Summary
```json
POST /api/news/summarize
{
  "url": "https://example.com/some-article"
}
```

### Smart Day Plan
```json
POST /api/planner/generate
{
  "city": "Mumbai"
}
```

### Text-to-Speech
```json
POST /api/tts/speak
{
  "text": "Good morning! Here is your weather report.",
  "lang": "en",
  "slow": false
}
```
→ Returns an `audio/mpeg` stream.

---

## Project Structure
```
udaya-backend/
├── app/
│   ├── main.py            # FastAPI app, CORS, router registration
│   ├── config.py          # Pydantic settings (reads .env)
│   ├── schemas.py         # All request/response Pydantic models
│   ├── routers/
│   │   ├── weather.py     # /api/weather/*
│   │   ├── news.py        # /api/news/*
│   │   ├── planner.py     # /api/planner/*
│   │   └── tts.py         # /api/tts/*
│   └── services/
│       ├── weather_service.py   # OpenWeather + Gemini analysis/forecast
│       ├── news_service.py      # NewsAPI + Gemini summarization
│       ├── planner_service.py   # SerpAPI events + Gemini day plan
│       └── tts_service.py       # gTTS → BytesIO MP3
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Docker

```bash
docker build -t udaya-backend .
docker run -p 8000:8000 --env-file .env udaya-backend
```
