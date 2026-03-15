import os

target_file = r"D:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

new_content = """import streamlit as st
import time
import uuid

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="EverTutor - AI Navigator",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session():
    if "app_started" not in st.session_state:
        st.session_state.app_started = False
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
        st.session_state.current_session_id = None

init_session()

def create_new_session(topic_name="New Learning Topic"):
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {
        "name": topic_name,
        "messages": [
            {"role": "assistant", "content": "Welcome! I'm EverTutor. What topic would you like to learn about today? (e.g., 'Python Iterators', 'Quantum Physics')"}
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

# ---------------------------------------------------------
# 1. LANDING PAGE (STARLINK BACKGROUND)
# ---------------------------------------------------------
if not st.session_state.app_started:
    st.markdown('''
    <style>
    /* Hide the sidebar and top header on the start page */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }

    /* Dynamic Starlink Background */
    .stApp {
        background-color: #040914 !important;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cdefs%3E%3Cstyle%3E.dot{fill:rgba(255,255,255,0.7);}.line{stroke:rgba(255,255,255,0.15);stroke-width:1;}%3C/style%3E%3C/defs%3E%3Ccircle class='dot' cx='60' cy='60' r='2'/%3E%3Ccircle class='dot' cx='240' cy='120' r='3'/%3E%3Ccircle class='dot' cx='120' cy='300' r='2'/%3E%3Ccircle class='dot' cx='340' cy='220' r='2.5'/%3E%3Cline class='line' x1='60' y1='60' x2='240' y2='120'/%3E%3Cline class='line' x1='240' y1='120' x2='340' y2='220'/%3E%3Cline class='line' x1='240' y1='120' x2='120' y2='300'/%3E%3Cline class='line' x1='60' y1='60' x2='120' y2='300'/%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600'%3E%3Cdefs%3E%3Cstyle%3E.dot{fill:rgba(100,200,255,0.5);}.line{stroke:rgba(100,200,255,0.1);stroke-width:0.5;}%3C/style%3E%3C/defs%3E%3Ccircle class='dot' cx='150' cy='150' r='1.5'/%3E%3Ccircle class='dot' cx='450' cy='250' r='2'/%3E%3Ccircle class='dot' cx='250' cy='450' r='1.5'/%3E%3Ccircle class='dot' cx='550' cy='500' r='1'/%3E%3Cline class='line' x1='150' y1='150' x2='450' y2='250'/%3E%3Cline class='line' x1='450' y1='250' x2='550' y2='500'/%3E%3Cline class='line' x1='450' y1='250' x2='250' y2='450'/%3E%3Cline class='line' x1='150' y1='150' x2='250' y2='450'/%3E%3C/svg%3E"),
            radial-gradient(circle at 50% 50%, rgba(10, 30, 70, 0.6) 0%, #040914 100%);
        animation: starlink_move 60s linear infinite;
        background-size: 400px 400px, 600px 600px, cover;
    }

    @keyframes starlink_move {
        0% { background-position: 0px 0px, 0px 0px, center; }
        100% { background-position: 400px 400px, -600px 600px, center; }
    }

    /* Start Button Styling */
    div.stButton > button {
        border-radius: 50px !important;
        padding: 1.2rem 3rem !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        background: rgba(30, 58, 138, 0.4) !important;
        border: 2px solid rgba(147, 197, 253, 0.4) !important;
        color: #fff !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3), inset 0 0 15px rgba(59, 130, 246, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: scale(1.05) !important;
        background: rgba(37, 99, 235, 0.6) !important;
        box-shadow: 0 0 30px rgba(96, 165, 250, 0.6), inset 0 0 20px rgba(59, 130, 246, 0.4) !important;
        border-color: rgba(147, 197, 253, 0.8) !important;
        color: white !important;
    }

    /* Title Styling */
    .hero-title {
        text-align: center;
        margin-top: 20vh;
        font-size: 5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #93c5fd, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        animation: glowtext 3s ease-in-out infinite alternate;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: #94a3b8;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    @keyframes glowtext {
        from { transform: scale(1); filter: drop-shadow(0 0 10px rgba(147,197,253,0.3)); }
        to { transform: scale(1.02); filter: drop-shadow(0 0 20px rgba(147,197,253,0.8)); }
    }
    </style>
    ''', unsafe_allow_html=True)

    # Layout for Start Page
    st.markdown("<div class='hero-title'>EverMemOS</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Adaptive Socratic AI powered by Cognitive Tracking Networks</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 INITIATE SESSION", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()

# ---------------------------------------------------------
# 2. MAIN APPLICATION
# ---------------------------------------------------------
else:
    # Custom CSS for Main App
    st.markdown('''
    <style>
    /* Restore Header */
    header[data-testid="stHeader"] { display: block !important; }

    /* Animated Gradient Background for Main App */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e3a8a, #0b2e59, #172554) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
        color: white;
    }

    /* Glassmorphism & Transparent Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Chat Input */
    .stChatInputContainer > div {
        background-color: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Sidebar Background Layering */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(15px) !important;
    }

    /* Metric boxes */
    div[data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: white !important;
    }

    .stMarkdown, p, h1, h2, h3, h4, h5, h6, li {
        color: #F8FAFC !important;
    }
    </style>
    ''', unsafe_allow_html=True)

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
            if st.button("🗑️ Reset All State / Exit", use_container_width=True):
                st.session_state.sessions = {}
                st.session_state.current_session_id = None
                st.session_state.app_started = False  # Go back to start screen
                st.rerun()

    # --- Main App Layout ---
    if not st.session_state.current_session_id or st.session_state.current_session_id not in st.session_state.sessions:
        # Prompt user to start their first conversation
        st.title("🦉 Welcome to EverTutor Dashboard!")
        st.markdown(
            "You are now inside the AI interface. **Please create a new topic from the sidebar** to begin experiencing adaptive Socratic learning."
        )
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.write("")
            if st.button("🚀 Quick Start: My First Session", use_container_width=True):
                create_new_session()
                st.rerun()

    else:
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
                                if prompt.strip().isdigit():
                                    idx = int(prompt.strip()) - 1
                                    if 0 <= idx < len(active_session["knowledge_tree"]):
                                        new_focus = active_session["knowledge_tree"][idx]
                                        active_session["current_focus"] = new_focus
                                        
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

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Added Starlink custom landing page!")