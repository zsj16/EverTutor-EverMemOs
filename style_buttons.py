import os

target_file = r"D:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# We want to add CSS specifically for the main application, or generally to the stApp.
# The user wants "create new topic", "new learning topic", "view details", etc. to have highly transparent blue background.
# Since the landing page has its own CSS inside the "if not st.session_state.app_started:" block,
# we need to inject CSS into the MAIN APPLICATION block "else:" or globally outside the if block.

main_app_marker = "# 2. MAIN APPLICATION"
main_app_idx = content.find(main_app_marker)

main_app_css = """
import streamlit as st

# Apply global custom styles for main app buttons
st.markdown('''
<style>
/* Style for all regular buttons in the sidebar and main app */
[data-testid="stSidebar"] div.stButton > button,
.main div.stButton > button {
    background-color: rgba(14, 165, 233, 0.1) !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    color: #e0f2fe !important;
    border-radius: 8px;
    backdrop-filter: blur(4px);
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] div.stButton > button:hover,
.main div.stButton > button:hover {
    background-color: rgba(14, 165, 233, 0.25) !important;
    border-color: rgba(56, 189, 248, 0.8) !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    color: white !important;
}
</style>
''', unsafe_allow_html=True)
"""

# Let's insert the css just after the main app marker.
if "/* Style for all regular buttons in the sidebar and main app */" not in content:
    replacement = f"{main_app_marker}\n{main_app_css}"
    content = content.replace(main_app_marker, replacement)
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected CSS for transparent blue buttons!")
else:
    print("CSS already injected.")
