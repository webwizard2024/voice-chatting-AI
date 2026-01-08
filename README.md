Smart Voice to Voice Chat Application

This project is a voice-enabled conversational chatbot developed using Python and Streamlit. It allows users to interact with an AI assistant using speech or text and receive spoken responses in real time.

The goal of this project is to demonstrate how speech recognition, generative AI, and text-to-speech can be integrated into a single interactive application.

Why This Project?

Voice-based interfaces are increasingly used in modern applications such as virtual assistants, accessibility tools, and smart systems. However, building a complete voice-to-voice system often feels complex for beginners.

This project provides a simple and practical implementation that shows how different components can work together to create a functional voice assistant using readily available libraries.

The Problem

Most basic chatbot implementations face several limitations:

Interaction is limited to text only

Speech input and output are handled poorly or inconsistently

Responses are too long or unnatural for spoken output

AI limitations are unclear, leading to misleading answers

Error handling for missing dependencies is often ignored

The Solution

This application addresses these issues by:

Supporting both voice and text input

Converting spoken input into text using speech recognition

Generating concise and conversational responses using Google Gemini

Converting AI responses back into speech

Handling missing libraries gracefully

Clearly defining what the assistant can and cannot answer

Features

Voice input using microphone

Text input as a fallback option

AI-powered responses using Google Generative AI (Gemini)

Text-to-speech output for spoken replies

Session-based chat history

Cleaned and shortened responses for natural speech

Option to clear conversation history

Technologies Used

Python

Streamlit

SpeechRecognition

Google Generative AI (Gemini)

gTTS (Google Text-to-Speech)

Application Workflow

The user speaks or types a message

Speech input is converted into text

The text is sent to the Gemini AI model

The model generates a short response

The response is cleaned for speech output

The system plays the spoken response

AI Behavior Rules

The assistant follows these rules:

Answers general knowledge questions

Does not provide real-time information such as weather, stock prices, or breaking news

Keeps responses short for better speech delivery

Uses a natural conversational tone

Clearly indicates when real-time access is not available

Installation

Clone the repository and install the required dependencies:

pip install -r requirements.txt

Requirements

The project uses the following Python packages:

streamlit>=1.28.0
SpeechRecognition>=3.10.0
google-generativeai>=0.3.0
gtts>=2.3.2

Running the Application
streamlit run app.py


Make sure you have added your Google Gemini API key in Streamlit secrets:

GEMINI_API_KEY = "your_api_key_here"

Limitations

The assistant does not have access to real-time data

Internet connection is required for AI and speech services

Microphone access must be enabled for voice input

Possible Enhancements

Multi-language support

Improved voice quality using neural TTS

Longer conversational memory

Mobile-friendly interface

Author

Ayesha Batool
Computer Science / AI
