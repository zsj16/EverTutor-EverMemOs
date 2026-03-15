import os

content = """import streamlit as st
import time

st.set_page_config(
    page_title="EverTutor - AI Navigator",
    page_icon="🦉",
    layout="wide"
)

# Custom CSS for Dark Blue/Transparent theme and Animated Background
st.markdown('''
<style>
/* Animated Gradient Background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e3a8a, #0b2e59, #172554);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

/* Glassmorphism & Transparent Chat Bubbles */
div[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}

/* Chat Input Bar Transparency */
.stChatInputContainer > div {
    background-color: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

/* Adjust general text colors */
.stMarkdown, p, h1, h2, h3, h4, h5, h6, li {
    color: #F8FAFC !important;
}

/* Metric boxes/Cards */
div[data-testid="stAlert"] {
    background-color: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: white !important;
}

/* Button style */
button[data-baseweb="button"] {
    background-color: rgba(30, 58, 138, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: white !important;
}
</style>
''', unsafe_allow_html=True)

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome! I'm EverTutor, your Socratic Guide. What topic would you like to conquer today? (e.g., 'Python iterators', 'React Hooks')"}
        ]
    if "cognitive_state" not in st.session_state:
        st.session_state.cognitive_state = {
            "mastered": ["Variables", "Loops"],
            "misconceptions": [],
            "unaware": ["Asynchronous flows"]
        }
    if "knowledge_tree" not in st.session_state:
        st.session_state.knowledge_tree = ""

init_session()

st.title("🦉 EverTutor (Cognitive Navigator)")
st.markdown("*Adaptive Socratic Tutor powered by **EverMemOS** — tracking your cognitive journey in real-time.*")
st.divider()

col_chat, col_context = st.columns([2, 1])

with col_chat:
    st.subheader("💬 Interactive Learning")
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Interactive Input
    if prompt := st.chat_input("Tell me what you'd like to learn or ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing memory & cognitive state..."):
                time.sleep(1.5) # Simulate processing
                
                # Mock response simulating tutoring
                reply = f"I see you mentioned '{prompt}'. Before I give you the answer, let's connect it to what you already know. Can you explain your current understanding of the underlying concept?"
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

with col_context:
    st.subheader("🧠 Cognitive Tracking")
    st.caption("Real-time diagnosis by EverMemOS")
    
    # Interactive metrics
    mastered_cnt = len(st.session_state.cognitive_state["mastered"])
    misconception_cnt = len(st.session_state.cognitive_state["misconceptions"])
    unaware_cnt = len(st.session_state.cognitive_state["unaware"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Mastered", mastered_cnt)
    col2.metric("🔴 Misconceptions", misconception_cnt)
    col3.metric("⚪ Unaware", unaware_cnt)

    with st.expander("🔍 View Details", expanded=True):
        st.success(f"**Mastered:**\\n\\n" + ("None yet" if not st.session_state.cognitive_state["mastered"] else ", ".join(st.session_state.cognitive_state["mastered"])))
        st.error(f"**Misconceptions:**\\n\\n" + ("None detected" if not st.session_state.cognitive_state["misconceptions"] else "\\n".join("- " + m for m in st.session_state.cognitive_state["misconceptions"])))
        st.info(f"**Blind Spots (Unaware):**\\n\\n" + ("None detected" if not st.session_state.cognitive_state["unaware"] else "\\n".join("- " + u for u in st.session_state.cognitive_state["unaware"])))
        
    st.divider()
    
    st.subheader("🌳 Knowledge Strategy")
    st.caption("Dynamically generated learning path")
    
    if st.button("✨ Simulate Graph Generation", use_container_width=True):
        with st.spinner("DeepSeek is shaping your curriculum..."):
            time.sleep(1)
            st.session_state.knowledge_tree = "1. **Core Concept** ➔ 2. **Basic Syntax** ➔ 3. **Advanced Usage** ➔ 4. **Common Pitfalls**"
            st.balloons() # Interactive success animation
            st.toast("Knowledge Tree updated successfully!", icon="✅")
            st.rerun()

    if not st.session_state.knowledge_tree:
        st.markdown("*Awaiting learning target...*")
    else:
        st.markdown(f"> {st.session_state.knowledge_tree}")
"""

with open(r'd:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fix applied successfully.")
