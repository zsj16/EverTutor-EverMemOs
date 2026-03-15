import os

content = """import streamlit as st
import json

# Configure page
st.set_page_config(
    page_title="EverTutor - Cognitive Navigator",
    page_icon="🦉",
    layout="wide"
)

# Custom CSS for Deep Blue, Transparent, and Animated Background
st.markdown('''
    <style>
    /* Animated Deep Blue Background */
    .stApp {
        background: linear-gradient(-45deg, #0a0f24, #102a5c, #001f3f, #051630);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f1f5f9;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Transparent Glassmorphism Containers */
    [data-testid="stVerticalBlock"] > div > div {
        background: rgba(16, 42, 92, 0.25) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1rem;
        transition: transform 0.3s ease;
    }
    [data-testid="stVerticalBlock"] > div > div:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Chat Messages Customization */
    [data-testid="stChatMessage"] {
        background: rgba(30, 58, 138, 0.15) !important;
        border: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 10px;
    }

    /* Headings & Text */
    h1, h2, h3, p, span, div {
        color: #e2e8f0 !important;
    }
    
    /* Interactive Input */
    .stChatInputContainer {
        background: rgba(2, 6, 23, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    </style>
''', unsafe_allow_html=True)

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your personal Cognitive Tutor. Tell me your learning goal (e.g., 'I want to learn Python async programming'), and I will customize a knowledge graph and guide you step-by-step."}
        ]
    if "cognitive_state" not in st.session_state:
        st.session_state.cognitive_state = {
            "mastered": [],
            "misconceptions": [],
            "unaware": []
        }
    if "knowledge_tree" not in st.session_state:
        st.session_state.knowledge_tree = ""

init_session()

# Title
st.title("🦉 EverTutor | Cognitive Navigator")
st.markdown("Adaptive Socratic AI Tutor powered by **EverMemOS** — *More than just answering, it tracks cognitive states.*")
st.divider()

# Layout: Left chat, Right knowledge & tracking
col_chat, col_context = st.columns([2, 1])

with col_chat:
    st.subheader("💬 Interactive Learning Session")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Interactive User Input
    if prompt := st.chat_input("What do you want to learn? Or what questions do you have?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # TODO: Integrate DeepSeek & EverMemOS
        placeholder_reply = "*(Analyzing cognitve state via EverMemOS...)*\\n\\nThis is a placeholder reply. Next, we will connect **EverMemOS** to read your historical cognitive states and use **DeepSeek** to generate Socratic guidance."
        
        st.session_state.messages.append({"role": "assistant", "content": placeholder_reply})
        with st.chat_message("assistant"):
            st.markdown(placeholder_reply)

with col_context:
    st.subheader("🧠 Cognitive Tracking")
    st.caption("Real-time diagnosis via EverMemOS")
    
    # Interactive Expanders instead of plain text
    with st.expander("🟢 **Mastered Concepts**", expanded=True):
        st.write("None yet" if not st.session_state.cognitive_state["mastered"] else "\\n".join(st.session_state.cognitive_state["mastered"]))
        
    with st.expander("🔴 **Misconceptions**", expanded=True):
        st.write("None yet" if not st.session_state.cognitive_state["misconceptions"] else "\\n".join(st.session_state.cognitive_state["misconceptions"]))
        
    with st.expander("⚪ **Blind Spots (Unaware)**", expanded=True):
        st.write("None yet" if not st.session_state.cognitive_state["unaware"] else "\\n".join(st.session_state.cognitive_state["unaware"]))
    
    st.divider()
    
    st.subheader("🌳 Knowledge Graph Progress")
    st.caption("AI dynamically generated learning path")
    if not st.session_state.knowledge_tree:
        st.info("Waiting to generate knowledge graph... Start chatting to build it!")
        # Add an interactive progress bar for visual flair
        st.progress(0, text="Knowledge Map Completion: 0%")
    else:
        st.markdown(st.session_state.knowledge_tree)
        st.progress(25, text="Knowledge Map Completion: 25%")
"""

with open(r"d:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated app.py successfully.")
