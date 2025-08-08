import google.generativeai as genai
import user_config  # Assuming user_config.py contains necessary configurations
# Configure your API key
genai.configure(api_key=user_config.api_key)

# Load the free Gemini model (Gemini Pro – text-only)
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini API Error:", e)
        return "Sorry, I couldn't get a response from Gemini."

