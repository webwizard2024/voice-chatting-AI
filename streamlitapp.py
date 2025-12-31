import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv
from gtts import gTTS
import io
import re

# --- Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Smart Voice Chat", page_icon="🎤", layout="wide")

st.title("🎤 Smart Voice Chat")
st.caption("👂 Speak → 🔊 Hear")

# --- Processing ---
audio_file = st.audio_input("🎤 Hold to speak")
text_input = st.chat_input("💬 Or type")

if audio_file or text_input:
    if audio_file:
        audio_bytes = audio_file.read()
        recognizer = sr.Recognizer()
        audio_source = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio_source as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data)
        except:
            user_text = "Sorry, try again."
    else:
        user_text = text_input

    st.session_state.messages.append({"role": "user", "content": user_text})

    # ✅ FIXED SYSTEM PROMPT - General knowledge OK, realtime NO
    system_prompt = """You are a helpful voice assistant.

RULES:
1. Answer general knowledge questions with basic facts (history, geography, culture, etc.)
2. ONLY say "no real-time access" for:
   - Weather forecasts
   - Breaking news  
   - Stock prices
   - Live sports scores
   - Current events after 2023
3. For general topics like countries, people, science: give clear basic info
4. Keep responses short (15-20 seconds speech)
5. Sound natural and conversational
6. No markdown formatting

User: {user_text}"""

    # Generate smart response
    full_response = ""
    for chunk in model.generate_content(system_prompt.format(user_text=user_text), stream=True):
        full_response += chunk.text

    # Clean for perfect voice
    def clean_voice(text):
        text = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*|`(.*?)`|__(.*?)__', r'\1', text)
        text = re.sub(r'[^\w\s\.\!\?,\-]', '', text)
        return re.sub(r'\s+', ' ', text.strip())[:150]

    voice_text = clean_voice(full_response)
    
    # Play voice only
    with st.spinner("🔊 Responding..."):
        tts = gTTS(voice_text, lang="en", slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_data = audio_buffer.getvalue()
    
    st.audio(audio_data, autoplay=True)
    st.session_state.messages.append({"role": "assistant", "content": voice_text, "audio": audio_data})

# Simple Sidebar
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("✅ Smart answers + honest limits!")




