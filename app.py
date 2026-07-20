import streamlit as st
import groq
import os
from duckduckgo_search import DDGS
from PIL import Image
import PyPDF2
import requests

# Page Config
st.set_page_config(
    page_title="Habib's Smart Vision & AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stChatMessage { border-radius: 12px; padding: 12px; margin-bottom: 10px; }
    .stButton>button { border-radius: 8px; background-color: #2563eb; color: white; border: none; }
    .stButton>button:hover { background-color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# Title Header
st.title("🤖 Habib's Smart Vision & Multi-Tool Agent")
st.caption("⚡ Powered by Groq | Vision, Documents, Weather, Search & Math")

# Initialize Groq Client
try:
    groq_client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY"))
except Exception as e:
    groq_client = None

# Helper function to read PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Helper function for Web Search
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except Exception:
        return "Search error occurred."

# Helper function for Weather
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
    except Exception:
        pass
    return "Weather info unavailable."

# Conversation Memory Initializer
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to Export Chat History as Text
def get_chat_history_text():
    chat_text = "--- Habib's Smart Vision & AI Agent Chat Export ---\n\n"
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "AI Agent"
        chat_text += f"{role}: {msg['content']}\n\n"
    return chat_text

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Agent Control Panel")
    st.info("💡 **Agent Capabilities:**\n- 📜 Export Chat\n- 🖼️ Vision Analysis\n- 📄 Document Reader\n- 🌐 Web Search\n- 🌦️ Real-time Weather\n- 🧮 Math Calculations")
    
    st.subheader("📁 Upload File / Image")
    uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf", "txt"])
    
    st.markdown("---")
    
    # Download Chat History Button
    if len(st.session_state.messages) > 0:
        chat_data = get_chat_history_text()
        st.download_button(
            label="📥 Download Chat History",
            data=chat_data,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# File Context Processing
file_context = ""
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type in ["png", "jpg", "jpeg"]:
        st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        file_context = f"[Attached Image: {uploaded_file.name}]"
    elif file_type == "pdf":
        pdf_text = read_pdf(uploaded_file)
        file_context = f"\n\n[Document Content]:\n{pdf_text[:3000]}"
        st.sidebar.success(f"✅ PDF Loaded: {uploaded_file.name}")
    elif file_type == "txt":
        txt_text = uploaded_file.read().decode("utf-8")
        file_context = f"\n\n[File Content]:\n{txt_text[:3000]}"
        st.sidebar.success(f"✅ Text Loaded: {uploaded_file.name}")

# Quick Suggestions
st.markdown("### 💡 Quick Try Options:")
col1, col2, col3 = st.columns(3)

prompt_input = None
with col1:
    if st.button("🌦️ Weather in Karachi"):
        prompt_input = "Karachi mein weather kaisa hai?"
with col2:
    if st.button("📰 Latest AI News"):
        prompt_input = "Latest AI news and updates globally"
with col3:
    if st.button("🧮 Solve: 25 * 4 + 150"):
        prompt_input = "Solve 25 * 4 + 150"

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle Input
user_query = st.chat_input("Yahan apna sawal likhein...")
final_query = user_query if user_query else prompt_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            response_text = ""
            query_lower = final_query.lower()
            
            if "weather" in query_lower or "mausam" in query_lower or "karachi" in query_lower:
                weather_info = get_weather("Karachi")
                response_text = f"Weather update: {weather_info}"
            elif "news" in query_lower:
                search_res = web_search(final_query)
                response_text = f"Latest findings:\n{search_res}"
            else:
                if groq_client:
                    try:
                        messages_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                        if file_context:
                            messages_payload.append({"role": "user", "content": file_context})
                        
                        chat_completion = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages_payload,
                            temperature=0.7
                        )
                        response_text = chat_completion.choices[0].message.content
                    except Exception as e:
                        response_text = f"API Error: {str(e)}"
                else:
                    response_text = f"Aapka sawal mil gaya: '{final_query}'. (Groq API Key configure nahi hai)."
            
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})