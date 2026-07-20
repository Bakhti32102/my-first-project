import os
import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image
from groq import Groq
from duckduckgo_search import DDGS

# Page Setup
st.set_page_config(page_title="Habib's Smart AI Agent", page_icon="🤖", layout="centered")

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("🤖 Agent Settings")
    st.info("Habib's Multi-Tool AI Agent powered by Groq")
    
    st.markdown("### 🛠️ Available Tools:")
    st.markdown("- 🖼️ **Image Vision:** Image upload & analysis")
    st.markdown("- 🌐 **Web Search:** Live news & facts")
    st.markdown("- 🌦️ **Weather Fetcher:** Real-time temperature")
    st.markdown("- 🧮 **Math Calculator:** Solve equations")
    
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "Aap Habib bhai ke Smart Assistant hain. Urdu/Hindi/Roman Urdu mein dostoana jawab dein."}
        ]
        st.rerun()

# Title Header
st.title("🤖 Habib's Smart Vision & Multi-Tool Agent")
st.caption("Class 7: Vision Enabled Multi-Tool Agent | Groq Powered")

# 1. Groq Client Setup (Safe secret loading)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

try:
    # Safe check for Streamlit secrets
    secrets_dict = getattr(st, "secrets", {})
    if "GROQ_API_KEY" in secrets_dict:
        GROQ_API_KEY = secrets_dict["GROQ_API_KEY"]
except Exception:
    pass

# Fallback: Check hardcoded env variable or prompt user
if not GROQ_API_KEY:
    st.error("🔑 Groq API Key nahi mili! Kripya `.streamlit/secrets.toml` file banayein.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Function to encode PIL Image to Base64
def encode_image(image):
    buffered = BytesIO()
    if image.mode in ('P', 'RGBA'):
        image = image.convert('RGB')
    
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- TOOLS DEFINITIONS ---
def get_current_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%t"
        res = requests.get(url)
        return f"{city} ka temperature {res.text.strip()} hai."
    except:
        return "Weather fetch nahi ho saka."

def calculate_math(expression):
    try:
        result = eval(expression)
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Math error: {e}"

def search_web(query):
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "Web search se koi result nahi mila."
        
        search_summary = ""
        for r in results:
            search_summary += f"Title: {r['title']}\nSnippet: {r['body']}\n\n"
        return search_summary
    except Exception as e:
        return f"Search error: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Kisi sheher ka live weather ya temperature maloom karne ke liye.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Koi bhi math ya calculation solve karne ke liye.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Live news, latest information, facts, ya internet search ke liye.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }
]

# 2. Session State Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Aap Habib bhai ke Smart Assistant hain. Urdu/Hindi/Roman Urdu mein dostoana jawab dein."}
    ]

# 3. Purani Messages Display Karein
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"] and msg.get("content"):
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], list):
                for part in msg["content"]:
                    if part.get("type") == "text":
                        st.write(part.get("text"))
                    elif part.get("type") == "image_url":
                        st.image(part["image_url"]["url"], caption="Uploaded Image", width=250)
            else:
                st.write(msg["content"])

# 4. Image Upload Widget
uploaded_file = st.file_uploader("🖼️ Photo upload karke poochain (Optional):", type=["jpg", "jpeg", "png"])

# 5. User Input Chat Box
if user_input := st.chat_input("Poochein (e.g. Is picture me kya hai?, Weather, Math)..."):
    
    # Process Image if Uploaded
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        base64_image = encode_image(image)
        
        # Structure multimodal message for Groq Vision
        message_content = [
            {"type": "text", "text": user_input},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        
        st.session_state.messages.append({"role": "user", "content": message_content})
        
        with st.spinner("🖼️ Image Analyze ki ja rahi hai..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=st.session_state.messages,
                )
                ai_reply = response.choices[0].message.content
                st.chat_message("assistant").write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.rerun()
            except Exception as e:
                st.error(f"Vision Error: {e}")

    else:
        # Standard Text / Tool Processing
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("AI Agent soch raha hai..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    tools=tools,
                    tool_choice="auto"
                )

                response_message = response.choices[0].message

                if response_message.tool_calls:
                    for tool_call in response_message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = json.loads(tool_call.function.arguments)
                        tool_out = ""

                        if fn_name == "get_current_weather":
                            city = fn_args.get('city')
                            st.info(f"⚡ Weather Tool Running for: {city}")
                            tool_out = get_current_weather(city)

                        elif fn_name == "calculate_math":
                            expr = fn_args.get('expression')
                            st.info(f"🧮 Math Tool Running for: {expr}")
                            tool_out = calculate_math(expr)

                        elif fn_name == "search_web":
                            q = fn_args.get('query')
                            st.info(f"🌐 Searching Web for: {q}")
                            tool_out = search_web(q)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_message.content or "Checking details...",
                        })

                        st.session_state.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_out
                        })

                    second_res = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=st.session_state.messages
                    )
                    ai_reply = second_res.choices[0].message.content
                    st.chat_message("assistant").write(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

                else:
                    ai_reply = response_message.content
                    st.chat_message("assistant").write(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")