import re

def modify_chat():
    filepath = r"d:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to replace the if prompt := st.chat_input(...): block
    target_start = '            # Interactive Input'
    
    # We'll use a split strategy to be perfectly safe
    parts = content.split('            # Interactive Input')
    if len(parts) != 2:
        print("Failed to find replacement target!")
        return
        
    tail_parts = parts[1].split('        with col_context:')
    if len(tail_parts) != 2:
        print("Failed to find bottom target!")
        return

    new_chat_logic = '''            # Interactive Input
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
                                mem_context = "\\n".join([f"[{r.get('create_time', 'Past')}] {r.get('content', '')}" for r in search_results])
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
                            
                            reply = f"**Summary:** {curr['summary']}\\n\\nHere is our connected strategy based on your request. Which area should we start?\\n"
                            for i, sub in enumerate(curr['subtopics']):
                                reply += f"**{i+1}.** {sub}\\n"
                            
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

        with col_context:'''

    final_content = parts[0] + new_chat_logic + tail_parts[1]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print("Injected Memory RAG successfully!")

if __name__ == "__main__":
    modify_chat()