# Smart Voice to Voice Chat Application

## Why This Project?

Voice-based interaction is becoming a core part of modern software systems, from virtual assistants to accessibility-focused applications. Despite this, building a complete voice-to-voice conversational system remains challenging for many beginners due to the number of components involved.

This project was developed to demonstrate how speech recognition, generative AI, and text-to-speech technologies can be combined into a single, working application using simple and widely available tools.

> “A practical system is often the best way to understand how individual AI components work together.”

---

## Context

Most conversational AI examples focus only on text-based interaction. While useful, they do not reflect how users naturally communicate in real-world environments.

This project shifts the focus toward **spoken interaction**, showing how an AI system can listen, reason, and respond through voice while maintaining clear limitations and predictable behavior.

---

## The Problem

Many beginner-level chatbot implementations suffer from common issues:

- Interaction is limited to text input and output  
- Speech handling is unreliable or inconsistent  
- Responses are too long or unsuitable for speech playback  
- AI limitations are unclear, leading to misleading results  
- Missing dependencies cause runtime failures  

---

## Design Philosophy

The design of this application follows a few key principles:

- Keep the system simple and understandable  
- Prefer clarity over feature overload  
- Ensure responses are suitable for spoken output  
- Fail gracefully when a component is unavailable  
- Be explicit about the assistant’s limitations  

These principles make the project suitable for learning, experimentation, and academic demonstration.

---

## The Solution

This application implements a complete voice-to-voice pipeline:

1. User provides input through voice or text  
2. Spoken input is converted into text  
3. Text is sent to a generative AI model (Google Gemini)  
4. The model generates a concise response  
5. The response is cleaned for speech output  
6. The system converts the response into audio and plays it  

---

## Key Features

- Voice input using a microphone  
- Text input as a fallback option  
- AI-generated responses using Google Generative AI  
- Text-to-speech output using gTTS  
- Session-based conversation history  
- Clear and enforced AI behavior rules  

---

## Technologies Used

- Python  
- Streamlit  
- SpeechRecognition  
- Google Generative AI (Gemini)  
- gTTS  

---

## Installation

Clone the repository and install dependencies using:

```bash
pip install -r requirements.txt
## Requirements

```txt
streamlit>=1.28.0
SpeechRecognition>=3.10.0
google-generativeai>=0.3.0
gtts>=2.3.2
Running the Application

Start the application with:

streamlit run streamlitapp.py


Add your API key in Streamlit secrets:

GEMINI_API_KEY = "your_api_key_here"

Limitations

The assistant does not provide real-time information

Internet access is required for AI and speech services

Microphone permission is required for voice input

Intended Use

This project is suitable for:

Academic demonstrations

Final year projects

Learning conversational AI systems

Voice interface experimentation

Portfolio presentation

Author

Aisha Habib
Computer Science / Artificial Intelligence
