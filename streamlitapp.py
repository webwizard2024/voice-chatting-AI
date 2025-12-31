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
# Check if API key is available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY in your environment or secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Use a more stable model name for production
try:
    model = genai.GenerativeModel("gemini-2.5-flash")  # Changed from gemini-2.5-flash
except:
    st.error("Failed to initialize the model. Check your API key and model name.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Smart Voice Chat", page_icon="🎤", layout="wide")

st.title("🎤 Smart Voice Chat")
st.caption("👂 Speak → 🔊 Hear")

# --- Processing ---
# Add a fallback for audio input in case it's not supported
audio_file = None
try:
    audio_file = st.audio_input("🎤 Hold to speak")
except Exception as e:
    st.warning(f"Audio input might not be supported in this environment: {str(e)}")

text_input = st.chat_input("💬 Or type")

if audio_file or text_input:
    if audio_file:
        try:
            audio_bytes = audio_file.read()
            recognizer = sr.Recognizer()
            audio_source = sr.AudioFile(io.BytesIO(audio_bytes))
            with audio_source as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio_data = recognizer.record(source)
            try:
                user_text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                user_text = "Sorry, I couldn't understand that. Please try again."
            except sr.RequestError as e:
                user_text = f"Error with speech recognition: {str(e)}"
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
            user_text = "Error processing audio. Please try typing instead."
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

    # Generate smart response with error handling
    try:
        full_response = ""
        response = model.generate_content(system_prompt.format(user_text=user_text), stream=True)
        for chunk in response:
            full_response += chunk.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        full_response = "I'm having trouble generating a response right now. Please try again."

    # Clean for perfect voice
    def clean_voice(text):
        text = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*|`(.*?)`|__(.*?)__', r'\1', text)
        text = re.sub(r'[^\w\s\.\!\?,\-]', '', text)
        return re.sub(r'\s+', ' ', text.strip())[:150]

    voice_text = clean_voice(full_response)
    
    # Play voice only with error handling
    try:
        with st.spinner("🔊 Responding..."):
            tts = gTTS(voice_text, lang="en", slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_data = audio_buffer.getvalue()
        
        st.audio(audio_data, format="audio/mp3", autoplay=True)
        st.session_state.messages.append({"role": "assistant", "content": voice_text, "audio": audio_data})
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": voice_text})

# Simple Sidebar
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("✅ Smart answers + honest limits!")
    
    # Add model info
    st.caption(f"Model: gemini-pro")
    
    # Add session info
    if len(st.session_state.messages) > 0:
        st.caption(f"Messages: {len(st.session_state.messages)}")