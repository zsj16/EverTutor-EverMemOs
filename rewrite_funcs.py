import sys
import json

with open('EverMemOS/ever_tutor/app.py', encoding='utf-8') as f:
    text = f.read()

start = text.find('def generate_knowledge_tree')
end = text.find('def diagnose_learning_state')

old_funcs = text[start:end]

new_funcs = """def generate_curriculum(topic):
    prompt = f\"\"\"You are an educational architect. A student wants to learn about "{topic}".
Provide a concise 2-sentence summary of this topic, and then break it down into EXACTLY 3 sequential learning subtopics.
Return ONLY valid JSON without markdown:
{{
    "summary": "Brief overview.",
    "subtopics": ["Subtopic 1", "Subtopic 2", "Subtopic 3"]
}}\"\"\"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        return json.loads(content)
    except:
        return {"summary": f"Learning path for {topic}", "subtopics": ["Basics", "Deep Dive", "Application"]}

def generate_chat_title(user_input):
    \"\"\"Call DeepSeek to generate a 2-word title for the chat session\"\"\"
    prompt = f"Summarize the following topic into exactly 2 words. Return ONLY the 2 words, no punctuation.\\nTopic: '{user_input}'"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )
        return response.choices[0].message.content.strip().replace('"', '')
    except:
        return user_input[:10] + "..."

def check_intent_and_focus(user_input, curriculum, current_focus):
    prompt = f\"\"\"A student and tutor are exploring a curriculum.
Curriculum: {json.dumps(curriculum)}
Current Focus: "{current_focus}"
Student Input: "{user_input}"

Tasks:
1. Check if the student's input completely derails from the OVERALL curriculum (out of bounds).
2. If it is out of bounds, provide a polite redirection message reminding them this is outside the current scope.
3. If the student is picking a subtopic from the list or continuing the current one, update new_focus to that subtopic.

Return ONLY valid JSON without markdown:
{{
    "is_out_of_bounds": true/false,
    "redirection_message": "...", 
    "new_focus": "The specific subtopic the student is on..."
}}\"\"\"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        return json.loads(content)
    except:
        return {"is_out_of_bounds": False, "redirection_message": "", "new_focus": current_focus}

"""

text = text.replace(old_funcs, new_funcs)

with open('EverMemOS/ever_tutor/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
