import streamlit as st
from langdetect import detect
import google.generativeai as genai
import os

# --- Streamlit App Configuration ---
st.set_page_config(page_title="Multilingual AI Chat", page_icon="🗣️")
st.title("🗣️ Multilingual AI Chatbot")
st.write("Chat with an AI that detects your language and responds in kind!")

# --- API Key Setup (for Streamlit deployment) ---
# In Streamlit Cloud, you set secrets via the UI. Locally, use .streamlit/secrets.toml.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("GOOGLE_API_KEY not found in Streamlit secrets. Please set it.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
try:
    gemini_model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}")
    st.stop()

# --- Language Detection Function ---
def detect_language(t):
    try:
        return detect(t)
    except:
        return "Could not detect language: An unknown error occurred"

# --- Multilingual AI Response Function ---
def multilingual_ai_response(u_in):
    d_lng = detect_language(u_in)
    if "Could not detect language" in d_lng:
        return f"Sorry, I couldn't understand the language of your input. Please try again. ({d_lng})"

    p_str = "You are an AI assistant. The user's input is in " + d_lng + ". Please respond to the following query in " + d_lng + ":\n\nUser: " + u_in + "\nAI:"

    try:
        response = gemini_model.generate_content(p_str)
        return response.text
    except Exception as e:
        return f"An error occurred while generating a response: {e}"

# --- Streamlit UI Elements ---
user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if user_input:
        with st.spinner("AI is thinking..."):
            response = multilingual_ai_response(user_input)
        st.write(f"**AI:** {response}")
    else:
        st.warning("Please enter your message!")

st.markdown("--- --- --- ---")
st.markdown("This app uses the Gemini API for responses and `langdetect` for language identification.")
import streamlit as st
from langdetect import detect
import google.generativeai as genai
import requests # New import for making API requests
import os

# --- Streamlit App Configuration ---
st.set_page_config(page_title="Multilingual AI Chat & Weather", page_icon="🗣️")
st.title("🗣️ Multilingual AI Chatbot & Weather")
st.write("Chat with an AI and get real-time weather information!")

# --- API Key Setup (for Streamlit deployment) ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except KeyError as e:
    st.error(f"Missing Streamlit secret: {e}. Please set it.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
try:
    gemini_model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}")
    st.stop()

# --- Language Detection Function ---
def detect_language(t):
    try:
        return detect(t)
    except:
        return "Could not detect language: An unknown error occurred"

# --- Multilingual AI Response Function ---
def multilingual_ai_response(u_in):
    d_lng = detect_language(u_in)
    if "Could not detect language" in d_lng:
        return f"Sorry, I couldn't understand the language of your input. Please try again. ({d_lng})"

    p_str = "You are an AI assistant. The user's input is in " + d_lng + ". Please respond to the following query in " + d_lng + ":\n\nUser: " + u_in + "\nAI:"

    try:
        response = gemini_model.generate_content(p_str)
        return response.text
    except Exception as e:
        return f"An error occurred while generating a response: {e}"

# --- Weather Function ---
def get_current_weather(city, api_key, units='metric'):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection Error: {e}"}
    except requests.exceptions.Timeout as e:
        return {"error": f"Timeout Error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}

# --- Streamlit UI Elements ---

st.header("Chat with AI")
user_input = st.text_input("You:", key="chat_input")

if st.button("Send Message"):
    if user_input:
        with st.spinner("AI is thinking..."):
            response = multilingual_ai_response(user_input)
        st.write(f"**AI:** {response}")
    else:
        st.warning("Please enter your message!")

st.markdown("--- --- --- ---")

st.header("Get Current Weather")
weather_city = st.text_input("Enter a city for weather information:", key="weather_city_input")

if st.button("Get Weather"):
    if weather_city:
        with st.spinner(f"Fetching weather for {weather_city}..."):
            weather_data = get_current_weather(weather_city, OPENWEATHER_API_KEY)
            if "error" in weather_data:
                st.error(weather_data["error"])
            else:
                if weather_data and weather_data['cod'] == 200:
                    main = weather_data['main']
                    weather = weather_data['weather'][0]
                    st.success(f"Current Weather in {weather_data['name']}:")
                    st.write(f"Temperature: {main['temp']}°C")
                    st.write(f"Feels like: {main['feels_like']}°C")
                    st.write(f"Description: {weather['description'].capitalize()}")
                    st.write(f"Humidity: {main['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                else:
                    st.error(f"Could not retrieve weather for {weather_city}. Please check the city name.")
    else:
        st.warning("Please enter a city name!")

st.markdown("--- --- --- ---")
st.markdown("This app uses the Gemini API for chat responses, `langdetect` for language identification, and OpenWeatherMap for weather data.")

