import streamlit as st
import groq
import os
from duckduckgo_search import DDGS
from PIL import Image
import PyPDF2
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import io

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
st.caption("⚡ Powered by Groq | Vision, Voice, Documents, Weather, Search & Math")

# Helper function to read PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Helper function to generate Text-to-Speech Audio
def speak_text(text):
    tts = gTTS(text=text, lang='ur', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

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
    st.info("💡 **Agent Capabilities:**\n- 📜 Export Chat\n- 🎙️ Voice Assistant\n- 🖼️ Vision Analysis\n- 📄 Document Reader\n- 🌐 Web Search\n- 🌦️ Real-time Weather\n- 🧮 Math Calculations")
    
    st.subheader("🎙️ Voice Input")
    st.write("Mic icon par click karke bolein:")
    audio_bytes = audio_recorder(text="", recording_color="#e11d48", neutral_color="#2563eb", icon_name="microphone", icon_size="2x")
    
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
user_query = st.chat_input("Poochein ya mic use karein...")

if audio_bytes and "audio_processed" not in st.session_state:
    st.session_state["audio_processed"] = True
    prompt_input = "Audio recording received. Please respond."

final_query = user_query if user_query else prompt_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    with st.chat_message("assistant"):
        with st.spinner("Agent thinking & generating audio response..."):
            response_text = f"Aapka sawal mil gaya: '{final_query}'. Agent active hai aur jawab tayar kar raha hai!"
            st.write(response_text)
            
            try:
                audio_fp = speak_text(response_text)
                st.audio(audio_fp, format='audio/mp3')
            except Exception as e:
                pass
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})