
import sys

with open('EverMemOS/ever_tutor/app.py', encoding='utf-8') as f:
    text = f.read()

start = text.find('    with col_context:')
end = text.find('        # --- Main Layout ---')

old_logic = text[start:end]

new_logic = '''    with col_context:
        # Add negative margin so the subtitle perfectly aligns with the chat subtitle "Interactive Learning"
        st.markdown("<h3 style='margin-top: -0.3rem;'>Knowledge Strategy</h3>", unsafe_allow_html=True)
        st.caption("Dynamically generated learning path")
        
        if not active_session.get("curriculum"):
            st.markdown("*Awaiting a specific learning target to generate curriculum...*")
        else:
            st.info(f"**Curriculum Summary:**\\n{active_session['curriculum']['summary']}")
            st.markdown("**Subtopics:**")
            for i, sub in enumerate(active_session['curriculum']['subtopics']):
                if active_session.get('current_focus') == sub:
                    st.markdown(f"**{i+1}. {sub} 🎯 (Current)**")
                else:
                    st.markdown(f"{i+1}. {sub}")

        st.divider()

        st.subheader("Cognitive Tracking")
        st.caption(f"Current Focus: {active_session.get('current_focus', 'None')}")

        # Interactive metrics
        mastered_cnt = len(active_session["cognitive_state"]["mastered"])
        misconception_cnt = len(active_session["cognitive_state"]["misconceptions"])
        unaware_cnt = len(active_session["cognitive_state"]["unaware"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Mastered", mastered_cnt)
        col2.metric("Misconceptions", misconception_cnt)
        col3.metric("Unaware", unaware_cnt)

        with st.expander("View Details", expanded=True):
            st.success(f"**Mastered:**\\n\\n" + ("None yet" if not active_session["cognitive_state"]["mastered"] else ", ".join(active_session["cognitive_state"]["mastered"])))
            st.error(f"**Misconceptions:**\\n\\n" + ("None detected" if not active_session["cognitive_state"]["misconceptions"] else "\\n".join("- " + m for m in active_session["cognitive_state"]["misconceptions"])))
            st.info(f"**Blind Spots (Unaware):**\\n\\n" + ("None detected" if not active_session["cognitive_state"]["unaware"] else "\\n".join("- " + u for u in active_session["cognitive_state"]["unaware"])))

'''

text = text.replace(old_logic, new_logic)

with open('EverMemOS/ever_tutor/app.py', 'w', encoding='utf-8') as f:
    f.write(text)

