import streamlit as st
import speech_recognition as sr
import time

# Language map
LANGUAGES = {
    "English (US)": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES"
}

# API map
APIS = {
    "Google Web Speech API": "google",
    "CMU Sphinx (Offline)": "sphinx"
}

# Save transcription
def save_to_file(text, filename="transcription.txt"):
    with open(filename, "w") as f:
        f.write(text)

# Transcribe
def transcribe_speech(api_choice, language_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = r.listen(source)

        try:
            if api_choice == "google":
                return r.recognize_google(audio, language=language_code)
            elif api_choice == "sphinx":
                return r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            return "⚠️ Could not understand audio."
        except sr.RequestError as e:
            return f"❌ API error: {e}"
        except Exception as e:
            return f"🚨 Unexpected error: {str(e)}"

# App UI
st.title("🗣️ Speech Recognition App")

api_choice_label = st.selectbox("Select Recognition API", list(APIS.keys()))
lang_choice_label = st.selectbox("Choose Language", list(LANGUAGES.keys()))
pause = st.button("Start Listening")

if pause:
    lang_code = LANGUAGES[lang_choice_label]
    api_code = APIS[api_choice_label]
    with st.spinner("Transcribing..."):
        result = transcribe_speech(api_code, lang_code)
        st.text_area("📝 Transcribed Text", result, height=150)
        if st.button("💾 Save Transcription"):
            save_to_file(result)
            st.success("Transcription saved to file.")

st.caption("Pause and resume by pressing 'Start Listening' each time.")
