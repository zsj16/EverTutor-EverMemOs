

import sys

with open('EverMemOS/ever_tutor/app.py', encoding='utf-8') as f:
    text = f.read()

start = text.find('            # --- Anti-Broadness Check for Empty Trees ---')
end = text.find('            # Refresh UI instantly so the right side Tracker and Sidebar updates')

old_logic = text[start:end]

new_logic = '''            if "curriculum" not in active_session:
                active_session["curriculum"] = None
                active_session["current_focus"] = "Awaiting initial topic..."

            if not active_session["curriculum"]:
                with st.spinner("Structuring curriculum..."):
                    curr = generate_curriculum(prompt)
                    active_session["curriculum"] = curr
                    active_session["current_focus"] = "Selecting Subtopic"
                    
                    reply = f"**Summary:** {curr['summary']}\\n\\nHere is our strategy. Which of these 3 areas would you like to start with?\\n"
                    for i, sub in enumerate(curr['subtopics']):
                        reply += f"**{i+1}.** {sub}\\n"
                    
                    st.markdown(reply)
                    active_session["messages"].append({"role": "assistant", "content": reply})
                    
                    mem_content = f"System set curriculum for {prompt}. Summary: {curr['summary']}. Subtopics: {curr['subtopics']}"
                    write_to_memory(mem_content, user_id=st.session_state.current_session_id)
                    
                    for sub in curr['subtopics']:
                        if sub not in active_session["cognitive_state"]["unaware"]:
                            active_session["cognitive_state"]["unaware"].append(sub)

            else:
                with st.spinner("Analyzing intent..."):
                    intent = check_intent_and_focus(prompt, active_session["curriculum"], active_session["current_focus"])
                    
                if intent.get("is_out_of_bounds"):
                    reply = intent.get("redirection_message", "That seems outside our current curriculum. Let's get back on track!")
                    st.markdown(reply)
                    active_session["messages"].append({"role": "assistant", "content": reply})
                    write_to_memory(f"User diverted topic. System redirected: {reply}", user_id=st.session_state.current_session_id)
                else:
                    new_focus = intent.get("new_focus")
                    if new_focus and new_focus != "Selecting Subtopic":
                        active_session["current_focus"] = new_focus
                    
                    with st.spinner("Updating cognitive map & generating response..."):
                        write_to_memory(f"Student asked: {prompt}", user_id=st.session_state.current_session_id)
                        
                        active_session["cognitive_state"] = diagnose_learning_state(
                            prompt, 
                            active_session["cognitive_state"], 
                            json.dumps(active_session["curriculum"])
                        )
                        
                        past_memory = search_memory(f"What did the student struggle with regarding {prompt} in {active_session['current_focus']}?", user_id=st.session_state.current_session_id)
                        
                        reply = generate_tutor_response(prompt, past_memory, active_session["cognitive_state"], active_session["current_focus"])
                        
                        st.markdown(reply)
                        active_session["messages"].append({"role": "assistant", "content": reply})
                        
                        write_to_memory(f"Tutor responded: {reply}", user_id=st.session_state.current_session_id)

'''
text = text.replace(old_logic, new_logic)

with open('EverMemOS/ever_tutor/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
