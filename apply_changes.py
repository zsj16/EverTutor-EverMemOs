import os

target_file = r"D:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

with open(target_file, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the init_session to include new state variables
old_init = """def init_session():
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

init_session()"""

new_init = """def init_session():
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
        st.session_state.knowledge_tree = None
    if "current_focus" not in st.session_state:
        st.session_state.current_focus = "Awaiting initial topic..."
    if "curriculum_summary" not in st.session_state:
        st.session_state.curriculum_summary = ""

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
    # Simple logic: if prompt length is long and doesn't share any word with the topic/subtopics, mark out of bounds
    keywords = " ".join(knowledge_tree).lower()
    return "pizza" in prompt.lower() or "weather" in prompt.lower() # example mock
"""

code = code.replace(old_init, new_init)

# Replace the chat logic
old_chat = """    # Interactive Input
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
                st.session_state.messages.append({"role": "assistant", "content": reply})"""

new_chat = """    # Interactive Input
    if prompt := st.chat_input("Tell me what you'd like to learn or ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            if st.session_state.knowledge_tree is None:
                with st.spinner("Generating Knowledge Strategy..."):
                    time.sleep(1)
                    curr = generate_curriculum(prompt)
                    st.session_state.knowledge_tree = curr["subtopics"]
                    st.session_state.curriculum_summary = curr["summary"]
                    st.session_state.current_focus = "Selecting Subtopic"
                    
                    # Saving classifications to memory
                    for sub in curr["subtopics"]:
                        if sub not in st.session_state.cognitive_state["unaware"]:
                            st.session_state.cognitive_state["unaware"].append(sub)
                    
                    reply = f"**Summary:** {curr['summary']}\\n\\nHere is our strategy. Which of these 3 areas would you like to start with?\\n"
                    for i, sub in enumerate(curr['subtopics']):
                        reply += f"**{i+1}.** {sub}\\n"
                    
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.rerun()
            else:
                with st.spinner("Analyzing intent..."):
                    time.sleep(1)
                    if is_out_of_bounds(prompt, st.session_state.knowledge_tree):
                        reply = "Your question seems to be out of the scope of our current Knowledge Strategy. Let's focus on our current topics, or do you want to create a new topic?"
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        # Match selection if it's a number
                        if prompt.strip().isdigit():
                            idx = int(prompt.strip()) - 1
                            if 0 <= idx < len(st.session_state.knowledge_tree):
                                new_focus = st.session_state.knowledge_tree[idx]
                                st.session_state.current_focus = new_focus
                                
                                # Add memory point here
                                mem_str = f"[Memory recorded: User selected {new_focus}]"
                                reply = f"Great! Let's focus on **{new_focus}**.\\n\\n*{mem_str}*\\n\\nPlease ask me anything about this or tell me what you already know."
                                st.markdown(reply)
                                st.session_state.messages.append({"role": "assistant", "content": reply})
                                st.rerun()
                        
                        reply = f"I see you mentioned '{prompt}' regarding **{st.session_state.current_focus}**. Let's connect it to what you already know. Can you explain your current understanding?"
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})"""


code = code.replace(old_chat, new_chat)

# Replace the right column layout
old_col = """with col_context:
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
        st.markdown(f"> {st.session_state.knowledge_tree}")"""

new_col = """with col_context:
    st.markdown("<h3 style='margin-top: -0.3rem;'>🌳 Knowledge Strategy</h3>", unsafe_allow_html=True)
    st.caption("Dynamically generated learning path")
    
    if not st.session_state.knowledge_tree:
        st.markdown("*Awaiting learning target...*")
    else:
        st.info(f"**Curriculum Summary:**\\n{st.session_state.curriculum_summary}")
        st.markdown("**Subtopics:**")
        for i, sub in enumerate(st.session_state.knowledge_tree):
            if st.session_state.current_focus == sub:
                st.markdown(f"**{i+1}. {sub} 🎯 (Current)**")
            else:
                st.markdown(f"{i+1}. {sub}")

    st.divider()

    st.subheader("🧠 Cognitive Tracking")
    # Subtitle referencing current topic
    focus_display = st.session_state.current_focus if st.session_state.current_focus != "Awaiting initial topic..." else "None"
    st.caption(f"Currently tracking understanding for: **{focus_display}**")
    
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
        st.info(f"**Blind Spots (Unaware):**\\n\\n" + ("None detected" if not st.session_state.cognitive_state["unaware"] else "\\n".join("- " + u for u in st.session_state.cognitive_state["unaware"])))"""

code = code.replace(old_col, new_col)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(code)

print("App updated successfully!")
