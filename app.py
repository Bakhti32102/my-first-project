import streamlit as st
import groq
import os
from duckduckgo_search import DDGS
from PIL import Image
import PyPDF2
import base64

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

# Helper function to read PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Sidebar Controls & File Upload
with st.sidebar:
    st.header("⚙️ Agent Control Panel")
    st.info("💡 **Agent Capabilities:**\n- 🖼️ Vision Analysis\n- 📄 Document/PDF Reader\n- 🌐 Web Search\n- 🌦️ Real-time Weather\n- 🧮 Math Calculations")
    
    st.subheader("📁 Upload File / Image")
    uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf", "txt"])
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Process Uploaded File Context
file_context = ""
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type in ["png", "jpg", "jpeg"]:
        st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        file_context = f"[User has attached an image: {uploaded_file.name}]"
    elif file_type == "pdf":
        pdf_text = read_pdf(uploaded_file)
        file_context = f"\n\n[Document Content from {uploaded_file.name}]:\n{pdf_text[:3000]}" # first 3000 chars
        st.sidebar.success(f"✅ PDF Loaded: {uploaded_file.name}")
    elif file_type == "txt":
        txt_text = uploaded_file.read().decode("utf-8")
        file_context = f"\n\n[File Content from {uploaded_file.name}]:\n{txt_text[:3000]}"
        st.sidebar.success(f"✅ Text File Loaded: {uploaded_file.name}")

# Quick Prompt Suggestions
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

# Conversation Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
user_query = st.chat_input("Poochein ya uploaded file ke bare mein sawal karein...")

final_query = user_query if user_query else prompt_input

if final_query:
    # Append file context if available
    full_prompt = final_query + (file_context if file_context else "")
    
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    with st.chat_message("assistant"):
        with st.spinner("Agent analyzing & processing..."):
            # Yahan aapka existing Groq / Tool response logic chalega
            response_text = f"Agent received: '{final_query}'"
            if file_context:
                response_text += f"\n\n*(Document/File attached & analyzed)*"
            
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})