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

