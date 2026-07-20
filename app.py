import streamlit as st
import groq
import os
from duckduckgo_search import DDGS

# Page Config
st.set_page_config(
    page_title="Habib's Smart Vision & AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    /* Dark / Clean Theme Touch */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        background-color: #2563eb;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: scale(1.02);
    }
    .quick-btn {
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Title Header
st.title("🤖 Habib's Smart Vision & Multi-Tool Agent")
st.caption("⚡ Powered by Groq | Vision, Weather, Web Search & Math")

# Sidebar
with st.sidebar:
    st.header("⚙️ Agent Control Panel")
    st.info("💡 **Agent Capabilities:**\n- 🖼️ Vision Analysis\n- 🌐 Live Web Search\n- 🌦️ Real-time Weather\n- 🧮 Math Calculations")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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
user_query = st.chat_input("Poochein (e.g. Weather, News, Math, Images)...")

# Handle Quick Prompts or Input
final_query = user_query if user_query else prompt_input

if final_query:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    # Agent Response Placeholder
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking & fetching tools..."):
            # Dummy or Actual Groq Logic Call
            # (Aapka existing Groq logic yahan rahega)
            response_text = f"Agent Response to: {final_query}" 
            st.write(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})