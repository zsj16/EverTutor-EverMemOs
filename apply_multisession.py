import os

new_content = """import streamlit as st
import time
import uuid

st.set_page_config(
    page_title="EverTutor - AI Navigator",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
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

/* Sidebar styling to look clear with dark theme */
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.9) !important;
}
</style>
''', unsafe_allow_html=True)

def create_new_session(topic_name="New Learning Topic"):
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "name": topic_name,
        "messages": [
            {"role": "assistant", "content": "Welcome! I'm EverTutor. What topic would you like to learn about today? (e.g., 'Python Iterators', 'Mitochondria')"}
        ],
        "cognitive_state": {
            "mastered": [],
            "misconceptions": [],
            "unaware": []
        },
        "knowledge_tree": None,
        "current_focus": "Awaiting initial topic...",
        "curriculum_summary": ""
    }
    st.session_state.current_session_id = session_id
    return session_id

def init_session():
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
        st.session_state.current_session_id = None

init_session()

def generate_curriculum(topic):
    # Mocking a call to generate directory structure
    return {
        "summary": f"This is a comprehensive overview of {topic}.",
        "subtopics": [f"{topic} Fundamentals", f"Advanced {topic}", f"{topic} Best Practices"]
    }

def is_out_of_bounds(prompt, knowledge_tree):
    if not knowledge_tree:
        return False
    return "pizza" in prompt.lower() or "weather" in prompt.lower() 

# --- Sidebar ---
with st.sidebar:
    st.title("📚 Learning Topics")
    if st.button("➕ Create New Topic", use_container_width=True):
        create_new_session()
        st.rerun()
        
    st.divider()
    
    if not st.session_state.sessions:
        st.info("No active topics right now. Start by creating one!")
    else:
        st.markdown("**Your Current Topics:**")
        for sid, s_data in list(st.session_state.sessions.items()):
            # Highlight the active session
            prefix = "🎯 " if sid == st.session_state.current_session_id else "📄 "
            if st.button(prefix + s_data['name'], key=f"btn_{sid}", use_container_width=True):
                st.session_state.current_session_id = sid
                st.rerun()
                
        st.divider()
        if st.button("🗑️ Clear All Memory / Topics", use_container_width=True):
            st.session_state.sessions = {}
            st.session_state.current_session_id = None
            st.rerun()

# --- Main Layout ---
if not st.session_state.current_session_id or st.session_state.current_session_id not in st.session_state.sessions:
    # --- Home Page Landing ---
    st.title("🦉 Welcome to EverTutor Space!")
    st.markdown('''
    ### Adaptive Socratic AI Tutor powered by **EverMemOS**
    
    It looks like you don't have an active learning session right now.
    
    With this system, you can maintain **multiple concurrent learning topics**. For each topic, the AI will build a personalized **Knowledge Strategy** dictionary and track your **Cognitive State** (Mastered concepts, Misconceptions, and Blind spots) entirely independently.
    ''')
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("")
        if st.button("🚀 Start your first learning session!", use_container_width=True):
            create_new_session()
            st.rerun()

else:
    # --- Active Topic View ---
    active_session = st.session_state.sessions[st.session_state.current_session_id]

    st.title(f"🦉 EverTutor - {active_session['name']}")
    st.markdown("*Adaptive Socratic Tutor powered by **EverMemOS** — tracking your cognitive journey in real-time.*")
    st.divider()

    col_chat, col_context = st.columns([2, 1])

    with col_chat:
        st.subheader("💬 Interactive Learning")
        
        # Display chat messages
        for msg in active_session["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Interactive Input
        if prompt := st.chat_input("Tell me what you'd like to learn or ask a question..."):
            active_session["messages"].append({"role": "user", "content": prompt})
            
            # Auto-rename session if it's the first real question
            if active_session["name"] == "New Learning Topic" and active_session["knowledge_tree"] is None:
                short_name = prompt[:20] + "..." if len(prompt) > 20 else prompt
                active_session["name"] = short_name

            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                if active_session["knowledge_tree"] is None:
                    with st.spinner("Generating Knowledge Strategy..."):
                        time.sleep(1)
                        curr = generate_curriculum(prompt)
                        active_session["knowledge_tree"] = curr["subtopics"]
                        active_session["curriculum_summary"] = curr["summary"]
                        active_session["current_focus"] = "Selecting Subtopic"
                        
                        # Saving classifications to memory
                        for sub in curr["subtopics"]:
                            if sub not in active_session["cognitive_state"]["unaware"]:
                                active_session["cognitive_state"]["unaware"].append(sub)
                        
                        reply = f"**Summary:** {curr['summary']}\\n\\nHere is our strategy. Which of these 3 areas would you like to start with?\\n"
                        for i, sub in enumerate(curr['subtopics']):
                            reply += f"**{i+1}.** {sub}\\n"
                        
                        st.markdown(reply)
                        active_session["messages"].append({"role": "assistant", "content": reply})
                        st.rerun()
                else:
                    with st.spinner("Analyzing intent..."):
                        time.sleep(1)
                        if is_out_of_bounds(prompt, active_session["knowledge_tree"]):
                            reply = "Your question seems to be out of the scope of our current topic Strategy. Let's focus on our current topic, or feel free to **Create a New Topic** from the Sidebar!"
                            st.markdown(reply)
                            active_session["messages"].append({"role": "assistant", "content": reply})
                        else:
                            # Match selection if it's a number
                            if prompt.strip().isdigit():
                                idx = int(prompt.strip()) - 1
                                if 0 <= idx < len(active_session["knowledge_tree"]):
                                    new_focus = active_session["knowledge_tree"][idx]
                                    active_session["current_focus"] = new_focus
                                    
                                    # Add memory point here
                                    mem_str = f"[Memory recorded: User selected {new_focus}]"
                                    reply = f"Great! Let's focus on **{new_focus}**.\\n\\n*{mem_str}*\\n\\nPlease ask me anything about this or tell me what you already know."
                                    st.markdown(reply)
                                    active_session["messages"].append({"role": "assistant", "content": reply})
                                    st.rerun()
                            else:
                                reply = f"I see you mentioned '{prompt}' regarding **{active_session['current_focus']}**. Let's connect it to what you already know. Can you explain your current understanding?"
                                st.markdown(reply)
                                active_session["messages"].append({"role": "assistant", "content": reply})

    with col_context:
        st.markdown("<h3 style='margin-top: -0.3rem;'>🌳 Knowledge Strategy</h3>", unsafe_allow_html=True)
        st.caption("Dynamically generated learning path")
        
        if not active_session["knowledge_tree"]:
            st.markdown("*Awaiting learning target...*")
        else:
            st.info(f"**Curriculum Summary:**\\n{active_session['curriculum_summary']}")
            st.markdown("**Subtopics:**")
            for i, sub in enumerate(active_session["knowledge_tree"]):
                if active_session["current_focus"] == sub:
                    st.markdown(f"**{i+1}. {sub} 🎯 (Current)**")
                else:
                    st.markdown(f"{i+1}. {sub}")

        st.divider()

        st.subheader("🧠 Cognitive Tracking")
        focus_display = active_session["current_focus"] if active_session["current_focus"] != "Awaiting initial topic..." else "None"
        st.caption(f"Currently tracking understanding for: **{focus_display}**")
        
        # Interactive metrics
        mastered_cnt = len(active_session["cognitive_state"]["mastered"])
        misconception_cnt = len(active_session["cognitive_state"]["misconceptions"])
        unaware_cnt = len(active_session["cognitive_state"]["unaware"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🟢 Mastered", mastered_cnt)
        col2.metric("🔴 Misconceptions", misconception_cnt)
        col3.metric("⚪ Unaware", unaware_cnt)

        with st.expander("🔍 View Details", expanded=True):
            st.success(f"**Mastered:**\\n\\n" + ("None yet" if not active_session["cognitive_state"]["mastered"] else ", ".join(active_session["cognitive_state"]["mastered"])))
            st.error(f"**Misconceptions:**\\n\\n" + ("None detected" if not active_session["cognitive_state"]["misconceptions"] else "\\n".join("- " + m for m in active_session["cognitive_state"]["misconceptions"])))
            st.info(f"**Blind Spots (Unaware):**\\n\\n" + ("None detected" if not active_session["cognitive_state"]["unaware"] else "\\n".join("- " + u for u in active_session["cognitive_state"]["unaware"])))
"""

with open(r'd:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated app.py with Sidebar, Homepage and Multi-Session support successfully.")

