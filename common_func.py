import pyttsx3
import speech_recognition as sr
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
engine.setProperty('voice', voices[0].id)  # ✅ FIXED TYPO

def speak(audio):
        engine = pyttsx3.init('sapi5')  # Use 'sapi5' for Windows TTS
        engine.setProperty('rate', 170)
        engine.setProperty('voice', voices[0].id)
        print("SPEAKING:", audio)
        engine.say(audio)
        engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)