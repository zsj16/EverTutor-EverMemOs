import os
import re

target_file = r"d:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the title and subtitle
content = re.sub(r'<h1 class="title">.*?</h1>', r'<h1 class="title">EverTutor</h1>', content)
content = re.sub(r'<p class="subtitle">.*?</p>', r'<p class="subtitle">Your personal learning Ai assistant</p>', content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Title updated successfully!")
