import os
import requests
from groq import Groq

# Try importing Streamlit safely (if running in Streamlit environment)
try:
    import streamlit as st
except ImportError:
    st = None

print("\n--- Class 1: Live AI Agent Started (Groq Powered) ---")

# 1. API Key load karein (Safe way - No Hardcoded Keys!)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if st and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

if not GROQ_API_KEY:
    print("\n[ERROR]: GROQ_API_KEY nahi mili! Kripya environment variable set karein ya secrets.toml file banayein.")
    exit()

# 2. Client Initialize Karein
client = Groq(api_key=GROQ_API_KEY)

# 3. User se sheher ka naam lena
city = input("Aap kis sheher ka mashwara chahte hain? ")

# 4. Live Weather API (wttr.in)
weather_url = f"https://wttr.in/{city}?format=%t"

try:
    # Internet se temperature fetch karna
    weather_response = requests.get(weather_url)
    temperature = weather_response.text.strip()
    
    print(f"\n[SYSTEM]: Live Data Fetched! {city} ka temperature is waqt {temperature} hai.")
    print("[SYSTEM]: AI Agent soch raha hai...\n")
    
    # 5. Prompt for AI
    prompt = f"Mera naam Habib hai. Meray sheher ({city}) ka temperature is waqt {temperature} hai. Mujhe batao aaj mujhe kis qism ke kapde pehannay chahiye? Boht short aur dostoana Urdu mein jawab do."
    
    # 6. Fast & Free LLM Call (llama-3.3-70b-versatile)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    print("==================================================")
    print(f"[AI AGENT JAWAB]:\n\n{chat_completion.choices[0].message.content}")
    print("==================================================")

except Exception as e:
    print(f"[SYSTEM ERROR]: {e}")