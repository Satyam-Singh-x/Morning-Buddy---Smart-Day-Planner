import streamlit as st
import random
import datetime
from mainlogic import get_weather , analyze_weather_with_gemini , get_news,summarize_news,smart_planner

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Udaya AI",
    page_icon="🌅",
    layout="centered"
)

# ---------------- HELPER FUNCTIONS ----------------

def get_random_quote():
    quotes = [
        "Every morning is a new beginning. Breathe, smile, and start again.",
        "Rise gently, today holds beautiful possibilities.",
        "Let today be calm, focused, and full of purpose.",
        "A peaceful morning leads to a powerful day.",
        "Wake up with gratitude and the day will unfold kindly.",
        "You don’t need to rush — good things take calm steps.",
        "Today is a fresh page; write something beautiful.",
        "Small positive thoughts can change your whole day.",
        "The future depends on what you do today. — Mahatma Gandhi",
        "Arise, awake, and stop not till the goal is reached. — Swami Vivekananda",
        "Dream, dream, dream. Dreams transform into thoughts and thoughts result in action. — Dr. A.P.J. Abdul Kalam",
    ]
    return random.choice(quotes)


def get_random_image():
    images = [
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9",
        "https://images.unsplash.com/photo-1497436072909-60f360e1d4b1",
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
        "https://images.unsplash.com/photo-1519681393784-d120267933ba"
    ]
    return random.choice(images)

# ---------------- HOME PAGE ----------------

def home_page():
    st.markdown(
        """
        <div style="text-align:center; padding:20px;">
            <h1>🌅 Udaya AI</h1>
            <h4 style="color:gray;">Where every morning begins with hope</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        get_random_image(),
        caption="🌞 A new day, a fresh mind, and endless possibilities ahead.",
        use_container_width=True
    )

    st.markdown("### 🌼 Thought for Today")
    st.success(f"“{get_random_quote()}”")

    st.markdown("---")

    st.markdown(
        """
        ### 🤝 Your Morning Buddy
        I’m here to help you:
        - 🌤 Check today’s weather  
        - 📰 Read news based on your interests  
        - 🧠 Plan your day smartly  
        - 🌟 Start your day with positivity  

        👉 Use the sidebar to begin.
        """
    )

# ---------------- OTHER PAGES ----------------

def weather_news_page():
    st.header("🌤️ Weather Update")
    st.write("Get the latest weather details for your city.")

    city = st.text_input("🌍 Enter your city name")

    if st.button("🔍 Get Weather"):
        if city.strip():
            with st.spinner("Fetching latest weather info..."):
                temperature_output = get_weather(city)
                ai_temperature= analyze_weather_with_gemini(temperature_output)

            st.markdown(
                f"""
                <div style="font-size:22px; font-weight:600; margin-top:10px;">
                    🌡️ {ai_temperature}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.success("✅ Weather data fetched successfully!")
        else:
            st.warning("⚠️ Please enter a valid city name.")





def interest_news_page():
    st.header("📰 News Based on Your Interest")
    interest = st.text_input(
        "Enter your interest:",
        "Technology, Health, Sports..."
    )
    if st.button("Fetch News"):
        if interest:
            articles=get_news(interest)
            titles=[]
            urls=[]
            image_url=[]
            for i in articles:
                titles.append(i["title"])
                urls.append(i["url"])
                image_url.append(i["urlToImage"])

            if not articles:
                st.error("No news articles found.")
            col1, col2, col3,col4, col5 = st.columns(5)
            with col1:
                st.subheader(titles[0])
                st.markdown('---')
                st.image(image_url[0])
                st.markdown('---')
                st.write('Read full article here.', urls[0])
                st.markdown('---')
                st.write(summarize_news(urls[0]))

            with col2:
                st.subheader(titles[1])
                st.markdown('---')
                st.image(image_url[1])
                st.markdown('---')
                st.write('Read full article here.', urls[1])
                st.markdown('---')
                st.write(summarize_news(urls[1]))

            with col3:
                st.subheader(titles[2])
                st.markdown('---')
                st.image(image_url[2])
                st.markdown('---')
                st.write('Read full article here.', urls[2])
                st.markdown('---')
                st.write(summarize_news(urls[2]))

            with col4:
                st.subheader(titles[3])
                st.markdown('---')
                st.image(image_url[3])
                st.markdown('---')
                st.write('Read full article here.', urls[3])
                st.markdown('---')
                st.write(summarize_news(urls[3]))

            with col5:
                st.subheader(titles[4])
                st.markdown('---')
                st.image(image_url[4])
                st.markdown('---')
                st.write('Read full article here.', urls[4])
                st.markdown('---')
                st.write(summarize_news(urls[4]))


        else:
            st.error("Please enter your interest.")





def smart_planner_page():
    st.header("🧠 Smart Day Planner")
    city = st.text_input("What is your city name?")
    if st.button("Plan My Day"):
        if city:
            smart_plan=smart_planner(city)
            st.subheader(f'Your Day Plan In {city}....')
            st.write(f'Date:{datetime.date.today()}')
            st.markdown('---')
            st.write(smart_plan)
            st.markdown('---')
            st.success('Have a nice day!')
        else:
            st.error("Please enter a city name.")


# ---------------- SIDEBAR ----------------

st.sidebar.title("🌅 Udaya AI")
st.sidebar.markdown("Your friendly morning assistant")
st.sidebar.markdown("---")

page_option = st.sidebar.radio(
    "Navigate",
    ("🏠 Home", "🌤 Weather", "📰 News", "🧠 Smart Planner")
)

# ---------------- ROUTING ----------------

if page_option == "🏠 Home":
    home_page()
elif page_option == "🌤 Weather":
    weather_news_page()
elif page_option == "📰 News":
    interest_news_page()
elif page_option == "🧠 Smart Planner":
    smart_planner_page()
