🌅 Udaya AI – Your Smart Morning Companion

Udaya AI is a smart, AI-powered morning assistant built using Streamlit + Gemini AI that helps users start their day with clarity, positivity, and planning.

It provides:

🌤 Intelligent weather insights

📰 News summaries based on interests

🧠 A smart daily planner

🔊 Voice narration for a hands-free experience

Designed to feel like a personal morning guide, not just another app.

✨ Features

🌤 Weather Assistant

Fetches real-time weather using OpenWeather API

Uses Gemini AI to generate:

Friendly weather explanations

Clothing & travel advice

Optional voice narration

📰 News Assistant

Fetches latest news based on user interests using NewsAPI.

Summarizes articles using Gemini AI

Clean and readable layout

Avoids unnecessary news clutter

🧠 Smart Day Planner

Generates a full-day itinerary

Uses:

Weather forecast

Local events

AI reasoning -> All information is collected by GEMINI using OpenWeather API and SerpAPI (No unnecesary extra details have to be provided)

Suggests:

Morning routines

Travel ideas

Food breaks

Leisure activities

Personalized and human-like planning

🔊 Voice Output

Uses Google Text-to-Speech (gTTS)

Converts AI responses into audio

Great for hands-free listening

🗂 Project Structure

📦 udaya-ai
│
├── app.py              # Streamlit frontend

├── mainlogic.py        # AI logic, APIs, planners

├── requirements.txt    # Dependencies

└── .streamlit/

    └── secrets.toml    # API keys (not committed)

⚙️ Tech Stack

Technology	Purpose

Streamlit	Web UI

Google Gemini	AI reasoning & summaries

OpenWeather API	Weather data

NewsAPI	News fetching

SerpAPI	Event discovery

gTTS	Voice narration

Python	Core backend

🔐 Environment Setup

1️⃣ Create .streamlit/secrets.toml

GOOGLE_API_KEY = "your_gemini_api_key"

OPENWEATHER_API_KEY = "your_openweather_key"

NEWS_API = "your_news_api_key"

SERP_API_KEY = "your_serp_api_key"


⚠️ Never commit this file to GitHub

2️⃣ Install Dependencies

pip install -r requirements.txt


requirements.txt

streamlit

requests

google-genai

gTTS

python-dotenv

3️⃣ Run the App

streamlit run app.py

🧠 How Udaya AI Works

🔹 Weather Flow

User → OpenWeather API → Gemini Analysis → Voice Output

🔹 News Flow

User Interest → NewsAPI → Gemini Summary

🔹 Smart Planner Flow

Weather + Events → Gemini → Full Day Plan

🧩 Key Design Decisions

✔ API calls minimized for efficiency

✔ Voice output optional

✔ Modular architecture

✔ Clean UI with Streamlit


🚀 Future Improvements

🌍 Auto location detection

🎧 Voice input support

📅 Calendar integration

🧠 Mood-based planning

☁️ Cloud caching

🧑‍💻 Author

Satyam
Creator of Udaya AI – Morning Buddy
Passionate about Generative AI, productivity tools & intelligent systems.
