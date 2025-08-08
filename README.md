# 🎙️ Voice Assistant — Streamlit UI

A Python-based voice assistant with a modern **Streamlit** user interface.  
It supports **text commands**, **uploaded audio commands**, and **local microphone input** for running your assistant logic.

## ✨ Features

- 🖊 **Text Command Mode** — Type a command and get instant AI-powered results.
- 🎧 **Upload Audio Mode** — Upload a `.wav`/`.mp3` file and let the assistant transcribe & execute it.
- 🎙 **Local Microphone Mode** — Speak commands directly (works when running locally on the same machine).
- 🔍 Search Google, Wikipedia, or YouTube.
- 📝 Manage a to-do list (`todo.txt`).
- 📅 Get the current date & time.
- 🔗 Open websites (YouTube, LinkedIn, ChatGPT, etc.).
- 🤖 Ask **Gemini AI** for answers.
- 📲 Send WhatsApp messages (via `pywhatkit`).
- 🔔 Desktop notifications for schedules.

## 📂 Project Structure

```
voice-assistant-ui/
│
├── app.py               # Streamlit UI script
├── gemini_request.py    # Should contain `ask_gemini(prompt)` implementation
├── todo.txt             # Your stored tasks
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🛠 Requirements

Install dependencies with:

```bash
pip install streamlit pyttsx3 SpeechRecognition plyer pyautogui wikipedia pywhatkit mtranslate image_generation
```

> **Note:**  
> - `pyttsx3` text-to-speech runs on the machine hosting the Streamlit app.  
> - `plyer.notification` shows desktop notifications only on the host machine.  
> - `gemini_request.py` must be implemented with your Gemini API logic.

## 🚀 How to Run Locally

1. Clone this repository:
```bash
git clone https://github.com/yourusername/voice-assistant-ui.git
cd voice-assistant-ui
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:
```bash
streamlit run app.py
```

4. Open your browser at:
```
http://localhost:8501
```

## 📌 Usage Modes

### 1️⃣ Text Command Mode
- Select **Text Command** from the radio menu.
- Type any command (e.g., `new task buy milk`) and press **Run Command**.

### 2️⃣ Upload Audio Mode
- Record an audio command (`.wav` or `.mp3`).
- Upload it in **Upload Audio** mode.
- The assistant will transcribe and execute it.

### 3️⃣ Local Microphone Mode
- Works **only** when running Streamlit locally.
- Select **Local Microphone** mode and press **Capture one command now** to speak.

## ⚠️ Limitations

- On **Streamlit Cloud**, microphone access is not available for real-time speech — use **Text** or **Upload Audio** mode there.
- `pyautogui` actions (like opening apps) run on the machine where the app is hosted, not the client browser.
- `pywhatkit.sendwhatmsg()` uses a hardcoded phone number/time — update it before use.

## 📜 License

This project is open-source and free to use for educational and personal purposes.

---

💻 Made with Python, Streamlit, and a bit of magic ✨
