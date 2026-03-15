import streamlit as st
import time
import uuid
import sys
import os
import asyncio
from dotenv import load_dotenv

# Ensure EverMemOS root is in Python Path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    # Also add the inner src folder where infra_layer resides
    SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
    if SRC_ROOT not in sys.path:
        sys.path.append(SRC_ROOT)

from demo.utils import SimpleMemoryManager
from openai import OpenAI

load_dotenv()

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

def sync_store_memory(group_id, content, sender):
    """Bridge to the async SimpleMemoryManager"""
    mgr = SimpleMemoryManager(group_id=group_id, scene="assistant")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(mgr.store(content, sender=sender))

def sync_search_memory(group_id, query, limit=5):
    mgr = SimpleMemoryManager(group_id=group_id, scene="assistant")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(mgr.search(query, limit=limit))

def get_llm_response(messages, context=""):
    # Read custom LLM configurations from EverMemOS .env
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("LLM_API_KEY")
    model_name = os.getenv("LLM_MODEL", "gpt-4o")

    # If the backend env didn't set a standard OPENAI_API_KEY, fallback to the deepseek one
    if not os.getenv("OPENAI_API_KEY") and api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    client = OpenAI(
        base_url=base_url,
        api_key=api_key or os.getenv("OPENAI_API_KEY")
    )
    
    sys_msg = {"role": "system", "content": f"You are EverTutor, a Socratic AI. You have memory of past events: {context}"}
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[sys_msg] + messages,
            temperature=0.7,
            stream=False
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"*(LLM Error: {str(e)} - Please check your .env keys)*"

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

import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. LANDING PAGE (DENSE BRAIN STARLINK BACKGROUND)
# ---------------------------------------------------------
import streamlit.components.v1 as components

if not st.session_state.app_started:
    st.markdown('''
    <style>
    /* Hide default Streamlit elements */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stApp > header { display: none !important; }
    
    /* Make app full dark */
    .stApp {
        background-color: #020617 !important;
        overflow: hidden;
    }
    
    /* Remove padding to let background be flush */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Target the iframe container natively generated by Streamlit to make it fixed */
    iframe {
        position: fixed !important;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 0 !important;
        border: none !important;
        pointer-events: auto !important;
    }

    /* Absolute positioning for the Streamlit button container */
    div.stButton {
        position: fixed;
        top: 75vh;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 99999 !important;
        text-align: center;
        display: flex;
        justify-content: center;
        width: 50%;
    }
    
    div.stButton > button {
        width: 50% !important;
        border-radius: 50px !important;
        padding: 1rem 2rem !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        background: rgba(14, 165, 233, 0.15) !important;
        border: 2px solid rgba(56, 189, 248, 0.6) !important;
        color: #f0f9ff !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.3), inset 0 0 15px rgba(14, 165, 233, 0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        transform: scale(1.05) translateY(-2px) !important;
        background: rgba(14, 165, 233, 0.4) !important;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.6), inset 0 0 25px rgba(56, 189, 248, 0.4) !important;
        border-color: rgba(125, 211, 252, 1) !important;
        color: #ffffff !important;
    }
    div.stButton > button:active {
        transform: scale(0.95) !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    html_code = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; padding: 0; background-color: #020617; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            #canvas-container { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
            #overlay { position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%); z-index: 10; text-align: center; pointer-events: none; width: 100%; }
            .title { font-size: 5rem; font-weight: 800; background: linear-gradient(135deg, #e0f2fe, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; text-shadow: 0 0 30px rgba(56,189,248,0.3); animation: pulse 4s infinite alternate; }
            .subtitle { font-size: 1.5rem; color: #94a3b8; margin-top: 1rem; font-weight: 400; letter-spacing: 2px; text-transform: uppercase;}
            @keyframes pulse { 0% { filter: brightness(1) drop-shadow(0 0 10px rgba(56,189,248,0.2)); } 100% { filter: brightness(1.2) drop-shadow(0 0 30px rgba(56,189,248,0.5)); } }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="overlay">
            <h1 class="title">EverTutor</h1>
            <p class="subtitle">Your personal learning Ai assistant</p>
        </div>
        <div id="canvas-container"></div>
        <script>
            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2('#020617', 0.001);
            
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 3000);
            camera.position.z = 800;

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor('#020617', 1);
            document.getElementById('canvas-container').appendChild(renderer.domElement);

            const particleCount = 2000;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);
            const sizes = new Float32Array(particleCount);
            
            for(let i = 0; i < particleCount; i++) {
                let theta = Math.random() * Math.PI * 2;
                let phi = Math.acos((Math.random() * 2) - 1);
                
                let r = 250 + Math.random() * 150;
                
                if (Math.abs(Math.sin(theta)) < 0.3) {
                    r *= 0.6 + (Math.abs(Math.sin(theta)) * 1.3);
                }
                if (Math.cos(phi) < -0.5) {
                    r *= 0.8;
                }

                let x = r * Math.sin(phi) * Math.cos(theta);
                let y = r * Math.cos(phi);
                let z = r * Math.sin(phi) * Math.sin(theta);
                
                x += (Math.random() - 0.5) * 40;
                y += (Math.random() - 0.5) * 40;
                z += (Math.random() - 0.5) * 40;

                positions[i*3] = x;
                positions[i*3+1] = y;
                positions[i*3+2] = z;
                
                sizes[i] = Math.random() * 2 + 1;
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

            const material = new THREE.PointsMaterial({
                color: 0x38bdf8,
                size: 2.5,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending
            });

            const particles = new THREE.Points(geometry, material);
            scene.add(particles);

            const lineMaterial = new THREE.LineBasicMaterial({
                color: 0x0ea5e9,
                transparent: true,
                opacity: 0.15,
                blending: THREE.AdditiveBlending
            });
            
            const lineGeo = new THREE.BufferGeometry();
            const linePos = [];
            const p = positions;
            const maxConnectDist = 65;
            
            for(let i=0; i<particleCount; i++) {
                let nodeConnects = 0;
                for(let j=i+1; j<particleCount; j++) {
                    if(nodeConnects > 4) break;
                    let dx = p[i*3] - p[j*3];
                    let dy = p[i*3+1] - p[j*3+1];
                    let dz = p[i*3+2] - p[j*3+2];
                    let dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
                    
                    if(dist < maxConnectDist) {
                        linePos.push(p[i*3], p[i*3+1], p[i*3+2]);
                        linePos.push(p[j*3], p[j*3+1], p[j*3+2]);
                        nodeConnects++;
                    }
                }
            }
            lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePos, 3));
            const lines = new THREE.LineSegments(lineGeo, lineMaterial);
            scene.add(lines);

            const glowGeo = new THREE.SphereGeometry(200, 32, 32);
            const glowMat = new THREE.MeshBasicMaterial({
                color: 0x0369a1,
                transparent: true,
                opacity: 0.05,
                blending: THREE.AdditiveBlending
            });
            const glowMesh = new THREE.Mesh(glowGeo, glowMat);
            scene.add(glowMesh);

            let mouseX = 0;
            let mouseY = 0;
            document.addEventListener('mousemove', (event) => {
                mouseX = (event.clientX - window.innerWidth / 2) * 1.5;
                mouseY = (event.clientY - window.innerHeight / 2) * 1.5;
            });

            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });

            let time = 0;
            function animate() {
                requestAnimationFrame(animate);
                time += 0.002;
                
                particles.rotation.y = time * 0.5;
                particles.rotation.z = time * 0.2;
                lines.rotation.y = time * 0.5;
                lines.rotation.z = time * 0.2;
                
                let pulseBase = 1 + (Math.sin(time * 15) * 0.02);
                particles.scale.set(pulseBase, pulseBase, pulseBase);
                lines.scale.set(pulseBase, pulseBase, pulseBase);
                glowMesh.scale.set(pulseBase*1.2, pulseBase*1.2, pulseBase*1.2);

                camera.position.x += (mouseX - camera.position.x) * 0.05;
                camera.position.y += (-mouseY - camera.position.y) * 0.05;
                camera.lookAt(scene.position);

                renderer.render(scene, camera);
            }
            animate();
        </script>
    </body>
    </html>
    '''
    
    # 1. Render background HTML natively to screen with fixed width/height 0 Streamlit layout
    components.html(html_code, height=0)
    
    # 2. Render actual Button. It will be positioned fixed automatically via the CSS above
    if st.button("INITIATE LINK"):
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

    /* Style for all regular buttons in the sidebar and main app */
    [data-testid="stSidebar"] div.stButton > button,
    .main div.stButton > button {
        background-color: rgba(14, 165, 233, 0.1) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #e0f2fe !important;
        border-radius: 8px !important;
        backdrop-filter: blur(4px) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover,
    .main div.stButton > button:hover {
        background-color: rgba(14, 165, 233, 0.25) !important;
        border-color: rgba(56, 189, 248, 0.8) !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
        color: white !important;
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
                
                # 1. Store user message in EverMemOS
                try:
                    sync_store_memory(st.session_state.current_session_id, prompt, sender="User")
                except Exception as e:
                    pass # Ensure UI doesn't crash if backend API is not running initially
                
                # Auto-rename session
                if active_session["name"] == "New Learning Topic" and active_session["knowledge_tree"] is None:
                    short_name = prompt[:20] + "..." if len(prompt) > 20 else prompt
                    active_session["name"] = short_name

                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                with st.chat_message("assistant"):
                    # 2. Retrieve Past Interactive Context
                    with st.spinner("🧠 Querying Episodic Memory..."):
                        mem_context = ""
                        try:
                            # Search the memory backend for relevant context
                            search_results = sync_search_memory(st.session_state.current_session_id, prompt, limit=3)
                            if search_results:
                                mem_context = "\n".join([f"[{r.get('create_time', 'Past')}] {r.get('content', '')}" for r in search_results])
                        except Exception:
                            pass
                            
                    if active_session["knowledge_tree"] is None:
                        with st.spinner("Generating Knowledge Strategy..."):
                            curr = generate_curriculum(prompt)
                            active_session["knowledge_tree"] = curr["subtopics"]
                            active_session["curriculum_summary"] = curr["summary"]
                            active_session["current_focus"] = "Selecting Subtopic"
                            
                            # Saving classifications to memory
                            for sub in curr["subtopics"]:
                                if sub not in active_session["cognitive_state"]["unaware"]:
                                    active_session["cognitive_state"]["unaware"].append(sub)
                            
                            reply = f"**Summary:** {curr['summary']}\n\nHere is our connected strategy based on your request. Which area should we start?\n"
                            for i, sub in enumerate(curr['subtopics']):
                                reply += f"**{i+1}.** {sub}\n"
                            
                            st.markdown(reply)
                            active_session["messages"].append({"role": "assistant", "content": reply})
                            # Store assistant reply in EverMemOS
                            try:
                                sync_store_memory(st.session_state.current_session_id, reply, sender="EverTutor")
                            except: pass
                            st.rerun()
                    else:
                        with st.spinner("EverTutor AI Processing..."):
                            # 3. Create context-aware generation using the standard LLM API
                            recent_msgs = active_session["messages"][-5:]
                            llm_messages = [{"role": m["role"], "content": m["content"]} for m in recent_msgs]
                            
                            if mem_context:
                                st.toast("Memory Retrieved! Integrating past context...", icon="🧠")
                                
                            reply = get_llm_response(llm_messages, context=mem_context)
                            
                            st.markdown(reply)
                            active_session["messages"].append({"role": "assistant", "content": reply})
                            
                            # 4. Store assistant reply in EverMemOS
                            try:
                                sync_store_memory(st.session_state.current_session_id, reply, sender="EverTutor")
                            except: pass

        with col_context:
            st.markdown("<h3 style='margin-top: -0.3rem;'>🌳 Knowledge Strategy</h3>", unsafe_allow_html=True)
            st.caption("Dynamically generated learning path")
            
            if not active_session["knowledge_tree"]:
                st.markdown("*Awaiting learning target...*")
            else:
                st.info(f"**Curriculum Summary:**\n{active_session['curriculum_summary']}")
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
                st.success(f"**Mastered:**\n\n" + ("None yet" if not active_session["cognitive_state"]["mastered"] else ", ".join(active_session["cognitive_state"]["mastered"])))
                st.error(f"**Misconceptions:**\n\n" + ("None detected" if not active_session["cognitive_state"]["misconceptions"] else "\n".join("- " + m for m in active_session["cognitive_state"]["misconceptions"])))
                st.info(f"**Blind Spots (Unaware):**\n\n" + ("None detected" if not active_session["cognitive_state"]["unaware"] else "\n".join("- " + u for u in active_session["cognitive_state"]["unaware"])))
