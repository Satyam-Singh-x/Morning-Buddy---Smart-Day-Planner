import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
import datetime
# -------------------- SETUP --------------------

load_dotenv()

OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")
NEWS_API = os.getenv("NEWS_API")
GEMINI_API = os.getenv("GOOGLE_API_KEY")



client = genai.Client(api_key=GEMINI_API)

# -------------------- WEATHER --------------------

def get_weather(city: str):
    """Fetch weather data from OpenWeather"""

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API}&units=metric"
    )

    res = requests.get(url)
    data = res.json()

    if res.status_code != 200:
        return {"error": True, "message": data.get("message", "Unknown error")}

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "condition": data["weather"][0]["description"]
    }


# -------------------- GEMINI WEATHER ANALYSIS --------------------

def analyze_weather_with_gemini(weather_data: dict):
    """
    Uses Gemini ONLY to analyze and give human-like advice.
    """

    prompt = f"""
You are a friendly weather assistant. First greet the user and provide the city name and country as a heading.

Here is the weather data:
{weather_data}

Your task:
1. Give a short and friendly weather report.
2. Suggest what to wear or carry.
3. Keep it natural and conversational.
4. Do NOT mention APIs or JSON.
5. Keep it concise and helpful.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -------------------- NEWS --------------------

def get_news(topic: str):
    """Fetch latest news headlines"""

    url =f"https://newsapi.org/v2/everything?q={topic}&pageSize=5&sortBy=publishedAt&apiKey={NEWS_API}"


    res = requests.get(url)
    data = res.json()

    if res.status_code != 200:
        return {"error": True, "message": data.get("message", "News error")}

    return data.get("articles", [])


# -------------------- NEWS SUMMARY (GEMINI) --------------------

def summarize_news(url: str):
    """Summarize a news article using Gemini"""

    prompt = f"""
Summarize this news article clearly in 4–5 lines.
Do not mention the source , article name etc.
Keep it clean and informative.

URL: {url}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text







#funtion to get forecast of entire day for an city and places to visit for a city

def get_forecasted_weather(city:str):
    """
    LLM TOOL:- fetches forecasted weather and tourist places to visit for the given city.

    args:
      city(str): city name(e.g. Delhi, Dehradun)_


    """
    try:

        grounding_tool=types.Tool(
            google_search=types.GoogleSearch()
        )

        config=types.GenerateContentConfig(
            tools=[grounding_tool]
        )



        response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
            Provide the detailed weather forecast for {city} on {datetime.date.today()}.
            Then also list the top recommended places to visit in {city} on the same date.
            Format the response clearly so it can be used by other planning agent
            """,
            config=config
        )

        return response.text
    except Exception as e:
        return{"error": str(e)}

#function to find the local events

def find_local_events(city: str):
    """
    find local events for the given city using an API.

    args:
    city(str): city name(e.g. Delhi, Dehradun)_


    """
    try:
        url = f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={os.getenv('SERP_API_KEY')}"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return{"error": str(e)}


#FUNCTION FOR SMART PLANNER:
def smart_planner(city):
    prompt = f"""
    You are a smart travel and event planner assistant.
    
    Your job is to create a personalized day itinerary for the user in a given {city} without asking him any questions as everything is provided to you.
    
    Budget: Plan the whole day considering the user to be upper middle class.
    
    Your goal is to suggest the best itinerary which enhances the knowledge ,social engagements, health along with fun ,calm, relaxng activities too. 
    
    You are given:
    
    Weather forecast for the {city} (with temperature, rain chances, humidity etc) and List of recommended places to visit in {city} on the same day..(Use the get_forecasted_weather function to get all the necessary weather details and famous tourist spots of {city})
    
    Upcoming events in the {city} (with title,date,time ,venue, description and link).(Use the find_local_events function provided to you to collect all the events with exact time venue links ,etc and use it to plan the day as instructed.)
    
    
    
    
    
   
    
    Instructions:
    
    Start with a warm friendly greeting acknowleding the user and  including the city name.  
    
    ALways use weather conditions to decide outdoor and indoor activities.
    
    Include healthy activities and events in Early mornings (like skating , gym, park visits etc)
    
    The day of user starts early morning (e.g 7 AM, 8 AM), you can also advise early morning activity events (like sports events or marathon events) and the end time can be midnight like 1 or 2 AM.
    
    Organize the plan chronologically (Morning -> afternoon ->Evening) and add time stamp of each event or plan.
    
    Do not mention the use of any given function in the response.
    
    
    
    
    Mix tourist attractions + events + leisure breaks so the day feels balanced.
    
    Plan events based on wide range of interests (e.g. history, art, wildlife, religious, adventure, food, technology etc.)
    
    Act as a tour guide and explain the history , importance (e.g cultural, educational,technological, etc.), benefits and probable fun of each activity.
    
    Try to plan budget friendly and value of money events with advising the ongoing discount offers going on at respective event links. If the event or plan cost is high then explain the fun experience and value of money with all important details (e.g. the cultural benefits, the quality of food at a particular restaurant etc.). 
    
    When recommending events, check if the event timing fits the user's availability.
    
    ALways include event links when mentioning them.
    
    Suggest Lunch/dinner breaks with general recommendations (local cuisine or malls).
    
    If multiple good options exist (eg 2 events at the same time),present them as choices.
    
    Keep the tone friendly and actionable and add sweet friendly emojis matching the events and plans , like a local guide making the plan.
    
    Dont conclude with any unnecessary question asking for more details or any improvements etc. 
    
    """
    response=client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[find_local_events,get_forecasted_weather]
        )
    )

    return response.candidates[0].content.parts[0].text







