import streamlit as st
import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections

# Ensure NLTK is ready
nltk.download('punkt', quiet=True)

# Sample chatbot patterns
pairs = [
    [
        r"hi|hello|hey",
        ["Hello there!", "Hi! How can I help?"]
    ],
    [
        r"what is your name?",
        ["I'm a speech-enabled chatbot!"]
    ],
    [
        r"how are you?",
        ["I'm doing great—ready to chat!"]
    ],
    [
        r"(.*) your name?",
        ["My name is Botty!"]
    ],
    [
        r"bye|exit",
        ["Goodbye!", "See you later!"]
    ],
]

# Create chatbot instance
chatbot = Chat(pairs, reflections)

# Function to transcribe voice
def transcribe_audio(language='en-US'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Speak now...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            return "❌ Sorry, I didn't catch that."
        except sr.RequestError as e:
            return f"⚠️ API error: {e}"

# Streamlit App
st.title("🗣️ Chat with Voice or Text")

option = st.radio("Choose input method:", ["Text", "Speech"])

user_input = ""

if option == "Text":
    user_input = st.text_input("Type your message:")
elif option == "Speech":
    if st.button("🎤 Start Listening"):
        user_input = transcribe_audio()

# Handle chatbot response
if user_input:
    st.write(f"**You:** {user_input}")
    response = chatbot.respond(user_input.lower())
    if response:
        st.write(f"**Botty:** {response}")
    else:
        st.write("**Botty:** I'm not sure how to respond to that.")
