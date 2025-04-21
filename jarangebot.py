
import os
import streamlit as st
import requests
from groq import Groq
from dotenv import load_dotenv

# --- Load API Keys from .env ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# --- Sarvam API config ---
SARVAM_API_URL = "https://api.sarvam.ai/translate"
SARVAM_HEADERS = {
    "Content-Type": "application/json",
    "API-Subscription-Key": os.getenv("SARVAM_API_KEY")
}

# --- Translation Functions using Sarvam Format ---
def translate_to_english(text):
    payload = {
        "input": text,
        "source_language_code": "auto",
        "target_language_code": "en-IN",  # fixed
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": False,
        "output_script": "roman",
        "numerals_format": "international"
    }
    response = requests.post(SARVAM_API_URL, json=payload, headers=SARVAM_HEADERS)

    try:
        data = response.json()
        print("Sarvam English Translation Response:", data)
        return data.get("translated_text", "[Translation Error to English]")
    except Exception as e:
        print("Error parsing English translation response:", e)
        return "[Translation Error to English]"

def translate_to_hindi(text):
    payload = {
        "input": text,
        "source_language_code": "en-IN",  # fixed
        "target_language_code": "hi-IN",  # fixed
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": False,
        "output_script": "fully-native",
        "numerals_format": "international"
    }
    response = requests.post(SARVAM_API_URL, json=payload, headers=SARVAM_HEADERS)

    try:
        data = response.json()
        print("Sarvam Hindi Translation Response:", data)
        return data.get("translated_text", "[Translation Error to Hindi]")
    except Exception as e:
        print("Error parsing Hindi translation response:", e)
        return "[Translation Error to Hindi]"
    
def translate_to_marathi(text):
    payload = {
        "input": text,
        "source_language_code": "en-IN",  # fixed
        "target_language_code": "mr-IN",  # fixed
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": False,
        "output_script": "fully-native",
        "numerals_format": "international"
    }
    response = requests.post(SARVAM_API_URL, json=payload, headers=SARVAM_HEADERS)

    try:
        data = response.json()
        print("Sarvam Marathi Translation Response:", data)
        return data.get("translated_text", "[Translation Error to Marathi]")
    except Exception as e:
        print("Error parsing Marathi translation response:", e)
        return "[Translation Error to Marathi]"


# --- Groq Chat Function ---
def get_response(prompt, user_lang="en"):
    try:
        if user_lang == "hi":
            prompt = translate_to_english(prompt)
        elif user_lang == "mr":
            prompt = translate_to_english(prompt)

        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": """You are AgriAI, an expert agricultural assistant for Indian farmers. Your purpose is to help farmers maximize their yields and income through sustainable practices.

Provide guidance on:
1. Crop selection based on soil type, season, climate zone, and market demand
2. Optimizing yields using data on soil nutrients, pH, humidity, temperature, and rainfall
3. Pest and disease management with both traditional and modern approaches
4. Water management and irrigation techniques appropriate for different regions
5. Relevant government schemes and subsidies based on farm size, income, crop type, and location
6. Organic farming practices and certification processes
7. Post-harvest storage and marketing strategies
8. Weather advisories and climate-smart agriculture techniques
9. Financial planning, loans, and insurance options for farmers
10. Modern agricultural technologies appropriate for small and medium farmers

When responding to farmers:
- Be respectful and practical in your advice
- Consider the constraints of small-scale farming (1-5 acres) common in India
- Provide specific, actionable recommendations rather than general advice
- Refer to crops and practices relevant to Indian agriculture
- Consider regional differences (North, South, East, West, Central India)
- Use simple language and avoid technical jargon when possible
- Include both traditional wisdom and modern scientific approaches
 

dont respoond to non agriculture related queries.
"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        response = chat_completion.choices[0].message.content

        if user_lang == "hi":
            response = translate_to_hindi(response)
        elif user_lang == "mr":
            response = translate_to_marathi(response)

        return response

    except Exception as e:
        return f"Error: {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="AgroSage Chat - Agriculture Assistant", page_icon="🌾")
st.title("🌾 AgroSage Chat - Your Agriculture Assistant")
st.write("Ask me anything about farming, crops, or agricultural practices!")

# --- Language Selection (Only English and Hindi) ---
st.sidebar.title("🌐 Language Settings")
language_options = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Marathi (मराठी)": "mr"
}
selected_lang = st.sidebar.radio("Choose your language", list(language_options.keys()))
user_lang_code = language_options[selected_lang]

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("How can I help you today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt, user_lang=user_lang_code)
            st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content":response})

