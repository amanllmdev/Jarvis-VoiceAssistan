import streamlit as st
import threading
import time
import os
import tempfile

# Your assistant logic imports (adjust to actual filenames)
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import gemini_request as gr
# import user_config  # optional

# ---------------------------
# Helper functions (adapted)
# ---------------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("rate", 170)
if len(voices) > 0:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    """Speak using pyttsx3 (server-side). Works when app runs locally."""
    try:
        tts = pyttsx3.init('sapi5')  # sapi5 is Windows; pyttsx3 will fallback otherwise
    except Exception:
        tts = pyttsx3.init()
    if len(voices) > 0:
        tts.setProperty("voice", voices[0].id)
    tts.setProperty("rate", 170)
    tts.say(text)
    tts.runAndWait()

def transcribe_audio_file(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="en-in")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# --- core command processor (extracted & simplified from your script) ---
def process_command(request, speak_response=True):
    """
    Process a single text request and return a textual response.
    speak_response: if True, speak() will be called (server-side).
    """
    request = (request or "").lower().strip()
    if not request:
        return "No command provided."

    # Copy the main branches you need; keep them short for UI output
    if "hello" in request:
        resp = "Welcome, how can I help you today?"
    elif "play music" in request:
        song_links = [
            "https://youtu.be/3TKghKSDnEM?si=PDDAMF9aGZd5_jea",
            "https://youtu.be/CExcLXD8Gy8?si=Dita4MPcS01d_Guf",
            "https://youtu.be/0RRWCxfkmtA?si=x78VnzX3M8r_BwG9",
            "https://youtu.be/eJ-LvX9HLrU?si=BViml6xYGgEPskB-"
        ]
        url = random.choice(song_links)
        webbrowser.open(url)
        resp = f"Playing music: {url}"
    elif "time kya hua hai" in request or "what time" in request:
        current_time = datetime.datetime.now().strftime("%H:%M")
        resp = f"The current time is {current_time}"
    elif "aaj date kya hai" in request or "what date" in request:
        current_date = datetime.datetime.now().strftime("%d %B")
        resp = f"Today's date is {current_date}"
    elif request.startswith("new task"):
        task = request.replace("new task", "").strip()
        if task:
            with open("todo.txt", "a", encoding="utf-8") as f:
                f.write(task + "\n")
            resp = f"Task added: {task}"
        else:
            resp = "You said new task but didn't provide content."
    elif "today's schedule" in request or "today schedule" in request or "schedule" == request:
        if os.path.exists("todo.txt"):
            with open("todo.txt", "r", encoding="utf-8") as f:
                tasks = f.read().strip()
            if tasks:
                try:
                    notification.notify(title="Today's Schedule", message=tasks, timeout=5)
                except Exception:
                    pass
                resp = "Today's schedule:\n" + tasks
            else:
                resp = "Your schedule is empty."
        else:
            resp = "No schedule file found."
    elif "open youtube" in request:
        webbrowser.open("https://www.youtube.com")
        resp = "Opening YouTube."
    elif "linkedin" in request:
        webbrowser.open("https://www.linkedin.com/in/amandeep-sharma-188189178")
        resp = "Opening LinkedIn."
    elif "search google" in request:
        q = request.replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={q}")
        resp = f"Searching Google for {q}"
    elif "send whatsapp" in request:
        # placeholder: update number/time as needed
        try:
            pwk.sendwhatmsg("+910123456789", "Hi, How are you", 16, 36)
            resp = "WhatsApp message scheduled."
        except Exception as e:
            resp = f"Failed to send WhatsApp: {e}"
    elif "gemini" in request or "gemini search" in request:
        prompt = request.replace("gemini", "").replace("gemini search", "").strip()
        if not prompt:
            resp = "What should I ask Gemini?"
        else:
            try:
                reply = gr.ask_gemini(prompt)
                resp = f"Gemini: {reply}"
            except Exception as e:
                resp = f"Gemini request failed: {e}"
    elif "wikipedia" in request:
        q = request.replace("wikipedia", "").replace("search wikipedia", "").strip()
        try:
            summary = wikipedia.summary(q, sentences=2)
            resp = summary
        except Exception as e:
            resp = f"Wikipedia lookup failed: {e}"
    elif "exit" in request or "stop" in request:
        resp = "Exit requested."
    else:
        resp = "Command not recognized."

    if speak_response and resp:
        # speak on the server machine (only works if server has audio)
        try:
            speak(resp)
        except Exception:
            pass

    return resp

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Voice Assistant UI", layout="centered")
st.title("🎙️ Voice Assistant — Streamlit UI")
st.write("Modes: Local Microphone (local run), Upload Audio, or Text input.")

mode = st.radio("Choose mode:", ("Text Command", "Upload Audio", "Local Microphone (local only)"))

if "log" not in st.session_state:
    st.session_state.log = []

def append_log(entry):
    st.session_state.log.append(entry)

# --- Text mode ---
if mode == "Text Command":
    txt = st.text_area("Type your command and press Run", height=120)
    if st.button("Run Command"):
        if txt.strip():
            append_log(f"> {txt}")
            result = process_command(txt, speak_response=True)
            append_log(result)
        else:
            st.warning("Please enter a command.")

# --- Upload audio ---
elif mode == "Upload Audio":
    uploaded_file = st.file_uploader("Upload a recorded audio file (.wav/.mp3)", type=["wav", "mp3", "m4a"])
    if uploaded_file:
        st.info("Transcribing uploaded audio...")
        # save temporary
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        transcribed = transcribe_audio_file(tmp_path)
        os.remove(tmp_path)
        if transcribed:
            append_log(f"> (audio) {transcribed}")
            result = process_command(transcribed, speak_response=True)
            append_log(result)
        else:
            append_log("Transcription failed or empty.")

# --- Local mic ---
elif mode == "Local Microphone (local only)":
    st.warning("Local microphone mode only works when Streamlit server and microphone are on the same machine.")
    if "listening" not in st.session_state:
        st.session_state.listening = False
    col1, col2 = st.columns([1,1])
    if col1.button("Start Listening (local)"):
        st.session_state.listening = True
    if col2.button("Stop Listening (local)"):
        st.session_state.listening = False

    if st.session_state.listening:
        st.info("Listening... (press Stop to end)")
        # Run a single blocking listen in the server process to capture one phrase
        if st.button("Capture one command now"):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                st.write("Listening — please speak now for ~5 seconds")
                audio = r.listen(source, timeout=7, phrase_time_limit=7)
            try:
                text = r.recognize_google(audio, language="en-in")
                append_log(f"> (mic) {text}")
                result = process_command(text, speak_response=True)
                append_log(result)
            except sr.UnknownValueError:
                append_log("Could not understand audio.")
            except sr.RequestError as e:
                append_log(f"Speech recognition error: {e}")

# Log display
st.markdown("### 🔁 Interaction Log")
for item in st.session_state.log[::-1]:
    st.write(item)

st.caption("Note: For real-time browser mic capture you need extra JS. This app supports local mic when run locally.")
