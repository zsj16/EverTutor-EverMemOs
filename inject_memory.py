import re
import sys

def inject():
    filepath = r"d:\ucberkeley\EverMemOs\EverMemOS\ever_tutor\app.py"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Imports
    imports_new = '''import streamlit as st
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

from demo.utils import SimpleMemoryManager
from openai import OpenAI

load_dotenv()'''
    content = re.sub(r'import streamlit as st\nimport time\nimport uuid', imports_new, content, count=1)

    # 2. Add Memory Wrapper Functions
    helpers = '''
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
    client = OpenAI()
    sys_msg = {"role": "system", "content": f"You are EverTutor, a Socratic AI. You have memory of past events: {context}"}
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",  # Fallback to standard OpenAI or DeepSeek if user configured it
            messages=[sys_msg] + messages,
            temperature=0.7,
            stream=False
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"*(LLM Error: {str(e)} - Please check your .env keys)*"
'''
    content = content.replace('init_session()\n', 'init_session()\n' + helpers)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
if __name__ == "__main__":
    inject()