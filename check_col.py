
import sys

with open('EverMemOS/ever_tutor/app.py', encoding='utf-8') as f:
    text = f.read()

start = text.find('with col_context:')
end = text.find('            # --- Developer Output End ---')

print(text[start:end])
