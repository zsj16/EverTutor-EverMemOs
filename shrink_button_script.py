import os
import re

target_file = r"D:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# Change the padding of the button to make it less wide
old_padding = "padding: 1rem 4rem !important;"
new_padding = "padding: 0.8rem 2rem !important;"

content = content.replace(old_padding, new_padding)

# I'll also check if regex is needed in case formatting differs slightly
content = re.sub(r'padding:\s*[0-9.]+rem\s+[0-9.]+rem\s+!important;', new_padding, content)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Button width reduced via CSS padding adjustment!")
