import streamlit as st
import os
import io
import re

# Try importing with error handling
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    st.error("⚠️ Speech recognition is not available. Please use text input.")

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    st.error("⚠️ Google Generative AI is not available.")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    st.error("⚠️ Text-to-speech is not available.")

# --- Setup ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    if GENAI_AVAILABLE:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
except KeyError:
    st.error("⚠️ API key not found. Please set GEMINI_API_KEY in your Streamlit secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="Smart Voice Chat", page_icon="🎤", layout="wide")

st.title("🎤 Smart Voice Chat")
st.caption("👂 Speak → 🔊 Hear")

# --- Processing ---
user_text = ""

# Audio input (if available)
if SR_AVAILABLE:
    audio_file = st.audio_input("🎤 Hold to speak")
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
            except:
                user_text = "Sorry, I couldn't understand that. Please try again."
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
            user_text = "Error processing audio. Please try typing instead."

# Text input (always available)
text_input = st.chat_input("💬 Or type")
if text_input:
    user_text = text_input

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})

    # System prompt
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

    # Generate response
    if GENAI_AVAILABLE:
        try:
            full_response = ""
            for chunk in model.generate_content(system_prompt.format(user_text=user_text), stream=True):
                full_response += chunk.text
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            full_response = "I'm having trouble generating a response right now. Please try again."
    else:
        full_response = "Google Generative AI is not available. Please check your installation."

    # Clean for voice
    def clean_voice(text):
        text = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*|`(.*?)`|__(.*?)__', r'\1', text)
        text = re.sub(r'[^\w\s\.\!\?,\-]', '', text)
        return re.sub(r'\s+', ' ', text.strip())[:150]

    voice_text = clean_voice(full_response)
    
    # Play voice
    if GTTS_AVAILABLE:
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
    else:
        st.session_state.messages.append({"role": "assistant", "content": voice_text})

# Sidebar
with st.sidebar:
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("✅ Smart answers + honest limits!")
    
    # Package status
    st.subheader("Package Status")
    st.write(f"Speech Recognition: {'✅' if SR_AVAILABLE else '❌'}")
    st.write(f"Google Generative AI: {'✅' if GENAI_AVAILABLE else '❌'}")
    st.write(f"gTTS: {'✅' if GTTS_AVAILABLE else '❌'}")