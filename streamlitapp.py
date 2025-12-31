import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from gtts import gTTS
import io
import re

# --- Setup with Streamlit Secrets ---
# Try to get API key from Streamlit secrets first, then fallback to .env for local development
try:
    # For Streamlit Cloud deployment
    api_key = st.secrets["GEMINI_API_KEY"]
except FileNotFoundError:
    # For local development - try to load from .env
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
except KeyError:
    st.error("GEMINI_API_KEY not found in Streamlit secrets. Please add it in your app settings.")
    st.stop()

if not api_key:
    st.error("""
    ### API Key Not Found
    
    **For Streamlit Cloud Deployment:**
    1. Go to your app's settings in Streamlit Cloud
    2. Add a new secret with key: `GEMINI_API_KEY`
    3. Set the value to your Gemini API key
    
    **For Local Development:**
    1. Create a `.env` file in your project root
    2. Add: `GEMINI_API_KEY=your_api_key_here`
    """)
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(
    page_title="Smart Voice Chat", 
    page_icon="🎤", 
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    .message {
        padding: 0.75rem 1rem;
        border-radius: 18px;
        margin-bottom: 0.75rem;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        margin-left: auto;
        text-align: left;
    }
    .assistant-message {
        background-color: #e9ecef;
        color: #333;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stAudio {
        margin-top: 0.5rem;
    }
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎤 Smart Voice Chat</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">💬 Type → 🔊 Hear</p>
</div>
""", unsafe_allow_html=True)

# Display chat history
if st.session_state.messages:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
            if "audio" in message:
                st.audio(message["audio"], format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #6c757d;">
        <h3>👋 Welcome to Smart Voice Chat!</h3>
        <p>Start a conversation by typing below.</p>
    </div>
    """, unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 💬 Type your message")

# Text input
user_input = st.chat_input("Type your message here...")

st.markdown('</div>', unsafe_allow_html=True)

# Processing
if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

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
    with st.spinner("🤔 Thinking..."):
        try:
            full_response = ""
            for chunk in model.generate_content(system_prompt.format(user_text=user_input), stream=True):
                full_response += chunk.text

            # Clean for voice
            def clean_voice(text):
                text = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*|`(.*?)`|__(.*?)__', r'\1', text)
                text = re.sub(r'[^\w\s\.\!\?,\-]', '', text)
                return re.sub(r'\s+', ' ', text.strip())[:150]

            voice_text = clean_voice(full_response)
            
            # Generate voice
            with st.spinner("🔊 Generating voice response..."):
                tts = gTTS(voice_text, lang="en", slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_data = audio_buffer.getvalue()
            
            # Add assistant message to session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": voice_text, 
                "audio": audio_data
            })
            
            # Auto-play the response
            st.audio(audio_data, autoplay=True, format="audio/mp3")
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.error(error_message)
    
    # Rerun to update the UI
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Chat History")
    
    # Display conversation statistics
    if st.session_state.messages:
        user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
        assistant_messages = [m for m in st.session_state.messages if m["role"] == "assistant"]
        
        st.metric("Messages", len(user_messages))
        st.metric("Responses", len(assistant_messages))
        
        st.markdown("---")
        
        # Show last 3 conversations
        st.markdown("### Recent Conversations")
        for i, msg in enumerate(st.session_state.messages[-6:], 1):
            if msg["role"] == "user":
                st.markdown(f"**Q{i//2 + 1}:** {msg['content'][:50]}...")
            else:
                st.markdown(f"**A{i//2 + 1}:** {msg['content'][:50]}...")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("✅ Smart answers + honest limits!")
    st.caption("🔒 Your API key is secure with Streamlit secrets")
    
    # Add a tip
    st.markdown("---")
    st.markdown("### 💡 Tip")
    st.caption("Type your questions clearly for better responses.")