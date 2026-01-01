Smart Voice Chat
A voice-enabled chat application powered by Google's Generative AI that allows users to interact through speech or text.

Features
🎤 Voice input with speech recognition
💬 Text input as an alternative
🔊 Text-to-speech response playback
🤖 AI-powered responses using Google's Gemini model
📱 Responsive web interface
🗑️ Chat history management


Installation
Prerequisites
Python 3.8 or higher
Google Generative AI API key
Local Setup
Clone the repository:
bash

git clone https://github.com/yourusername/voice-chatting-ai.git
cd voice-chatting-ai
Create a virtual environment:
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required packages:
bash

pip install -r requirements.txt
Set up your environment variables:
Create a .env file in the root directory
Add your Google Generative AI API key:

GEMINI_API_KEY=your_api_key_here
Run the application:
bash

streamlit run streamlitapp.py
Deployment on Streamlit Cloud
Push your code to a GitHub repository
Create a requirements.txt file with the following content:

streamlit>=1.28.0
SpeechRecognition>=3.10.0
google-generativeai>=0.3.0
gtts>=2.3.2
Go to Streamlit Cloud and click "New app"
Connect your GitHub repository and select the file path
In the "Advanced settings" section, add your API key as a secret:
Click "Edit secrets"
Add a new secret with the name GEMINI_API_KEY
Enter your actual API key as the value
Click "Deploy" and wait for the deployment to complete
Troubleshooting
ModuleNotFoundError for speech_recognition
If you encounter this error during deployment:

Make sure your requirements.txt file includes SpeechRecognition>=3.10.0 (with capital S and R)
Ensure the requirements.txt file is in the root directory of your project
Avoid including PyAudio in your requirements as it can cause issues on Streamlit Cloud
Alternative Text-Only Version
If you continue to have issues with the speech recognition package, you can deploy a text-only version by:

Removing SpeechRecognition from your requirements.txt
Using the alternative code provided in the repository that handles the missing package gracefully
Project Structure

voice-chatting-ai/
├── streamlitapp.py       # Main application file
├── requirements.txt      # Required packages
├── README.md            # This file
└── .env                 # Environment variables (not tracked in git)
Dependencies
streamlit: Web application framework
SpeechRecognition: Speech-to-text conversion
google-generativeai: Google's Generative AI SDK
gtts: Google Text-to-Speech
How It Works
The user provides input through voice or text
Voice input is converted to text using speech recognition
The text is sent to Google's Generative AI model
The AI response is processed and formatted for speech
The response is converted to speech and played back to the user
