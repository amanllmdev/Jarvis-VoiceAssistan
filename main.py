import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
import  os
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import user_config  # Assuming user_config.py contains necessary configurations
import smtplib
import ssl
import gemini_request as gr # Assuming gemini_request.py contains the ask_gemini function
import image_generation as  ig# Importing the image generation module
import mtranslate



# Initialize TTS engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
engine.setProperty('voice', voices[0].id)  # ✅ FIXED TYPO

def speak(audio):
        audio=mtranslate.translate(audio, to_language="hi",from_language="en-hi")  # Translate to Hindi
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

    try:
        content = r.recognize_google(audio, language='en-in')
        print("You said:", content)
        content=mtranslate.translate(content, to_language="en-in")  # Translate to Hindi
        print("You said:", content)
        return content.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error. Try again later.")
        return ""

def main_process():
    speak("Voice assistant activated. Say something.")
    while True:
        request = command().lower()

        if "hello" in request:
            speak("Welcome, How can I help you today?")

        elif "play music" in request:
            speak("Playing music")
            song_links = [
                "https://youtu.be/3TKghKSDnEM?si=PDDAMF9aGZd5_jea",
                "https://youtu.be/CExcLXD8Gy8?si=Dita4MPcS01d_Guf",
                "https://youtu.be/0RRWCxfkmtA?si=x78VnzX3M8r_BwG9",
                "https://youtu.be/eJ-LvX9HLrU?si=BViml6xYGgEPskB-"
            ]
            webbrowser.open(random.choice(song_links))

        elif "time kya hua hai" in request:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}")

        elif "aaj date kya hai" in request:
            current_date = datetime.datetime.now().strftime("%d %B")
            speak(f"Today's date is {current_date}")

        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task:
                with open("todo.txt", "a", encoding='utf-8') as file:
                    file.write(task + "\n")
                speak("Task added successfully: " + task)
            else:
                speak("You said new task, but didn't tell me what to write.")
        
        elif "today's schedule" in request:
            with open("todo.txt", "r", encoding='utf-8') as file:
                 speak("Today's schedule is as follows:"+file.read())
        
        
        elif "schedule" in request:
                try:
                    if os.path.exists("todo.txt"):
                        with open("todo.txt", "r", encoding='utf-8') as file:
                            tasks = file.read().strip()
                        if tasks:
                             print("Today's schedule is:")
                             notification.notify(
                                title="Today's Schedule",
                                message=tasks,
                                timeout=10
                              ) 
                             
                        else:
                            speak("Your schedule is empty.")
                    else:
                        speak("No schedule file found.")
                except Exception as e:
                    print("Error while reading schedule:", e)
                    speak("There was an error while reading your schedule.")
        elif "exit" in request or "stop" in request:
            speak("Okay, shutting down. Bye!")
            break
        elif  "open youtube" in request:
               webbrowser.open("https://www.youtube.com")
        
        elif "linkedin kholo" in request or "open linkedin" in request:
               webbrowser.open("https://www.linkedin.com/in/amandeep-sharma-188189178")

        elif "chatgpt kholo" in request or "open chatgpt" in request or "chat gpt kholo" in request:
               webbrowser.open("https://chat.openai.com/chat")
         
        elif  "search google" in request:
             request= request.replace("jarvis", "").strip()
             request= request.replace("search google ", "").strip()
             speak("Searching google for " + request)
             webbrowser.open(f"https://www.google.com/search?q={request}")
             
        elif  "send whatsapp" in request:
              pwk.sendwhatmsg("+910123456789", "Hi, How are you", 16, 36)
              
        elif "gemini search" in request or "jarvis" in request:
           prompt = request.replace("gemini", "").strip()
           if prompt:
              speak("Thinking...")
              reply = gr.ask_gemini(prompt).replace("**", "").replace("*", "")
              response = reply.split("\n")
              if len(response)<=2:
                  speak(reply)
              else:   
                      print("Gemini says:", reply)
           else:
              speak("What should I ask Gemini?")
      
         
        elif "generate image" in request:
            prompt = request.replace("generate image", "").strip()
            if prompt:
                speak(f"Generating image for: {prompt}")
                ig.generate_image(prompt)
            else:
                speak("Please tell me what image to generate.")      
        elif  "open" in request:
             query= request.replace("open", "").strip()
             pyautogui.press("super")
             pyautogui.typewrite(query)
             pyautogui.sleep(2)
             pyautogui.press("enter")
             
        elif  "wikipedia" in request:
             request= request.replace("jarvis", "").strip()
             request= request.replace("search wikipedia ", "").strip()
             speak("Searching Wikipedia for " + request)
             result=wikipedia.summary(request, sentences=2)
             speak(result)
             
        
             
        
             
    else:
            speak("Command not recognized. Try again.")

# Start the assistant
main_process()
