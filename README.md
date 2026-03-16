# 🦉 EverTutor: AI-Powered Socratic Learning Navigator

EverTutor is an intelligent, adaptative educational assistant designed to guide users through complex topics using the Socratic method. Featuring a stunning 3D WebGL interface and deep cognitive tracking, it evaluates the user's understanding in real-time, mapping out their progression through a dynamically generated curriculum.

## 🌟 Features
- **Adaptive Curriculum Generation**: Automatically creates a structured learning path ("Knowledge Strategy") based on any user-provided topic.
- **Cognitive Tracking**: Real-time evaluation of user's "Mastered" concepts, "Misconceptions", and "Blind Spots (Unaware)".
- **Socratic Interaction**: Guides users to find answers themselves by asking probing questions rather than just spoon-feeding information.
- **Immersive UI**: Full dark-mode Streamlit application featuring an interactive 3D particle network landing page built with Three.js.
- **Persistent Episodic Memory**: Never loses track of your progress thanks to deep integration with the EverMemOS memory backend.

---

## 🧠 How EverMemOS Powers Our Solution

Traditional chat-based tutors suffer from context-window amnesia. EverTutor eliminates this by leveraging **EverMemOS** as its core cognitive engine:

1. **Episodic Memory Storage**: Every interaction (both user questions and AI responses) is securely persisted to the vector knowledge base using `SimpleMemoryManager(scene="assistant").store()`.
2. **Dynamic Context Retrieval**: When a user asks a new question, EverTutor executes a semantic similarity search (`.search(query, limit=3)`) against their past episodic memory. This enriched context is dynamically injected into the LLM system prompt. 
3. **Cross-Session Continuity**: By retrieving relevant historical data, the tutor can "remember" analogies that worked well yesterday, reference past struggles, and avoid repeating debunked misconceptions—virtually mimicking a long-term human mentor.

---

## 🛠️ Code Logic & Architecture

- **Frontend Interface (`app.py`)**: Built entirely in Python using Streamlit for rapid prototyping, combined with embedded HTML/JS for the WebGL landing page background.
- **Memory Sync Bridge**: EverMemOS operates asynchronously, but Streamlit UI loops are strictly synchronous. EverTutor employs custom event-loop wrapper functions (`sync_store_memory` and `sync_search_memory`) via `asyncio.get_event_loop().run_until_complete()` to provide a seamless bridge.
- **LLM Client Routing**: The intelligence layer utilizes the standard `OpenAI()` Python client, but intercepts instantiation via a custom `get_llm_response` function that dynamically scopes API configurations (`LLM_BASE_URL`, `LLM_API_KEY`) from `.env`. This ensures zero-friction compatibility with DeepSeek and other diverse LLM endpoints.

---

## 🚀 Setup Setup & Installation

### 1. Prerequisites
- Python 3.10+
- The **EverMemOS Core Backend** must be running locally. 

### 2. Configure Environment Options
Create or update the `.env` file at the root directory of your project with the following properties (Example targeting DeepSeek):

```env
LLM_PROVIDER=openai
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=your_api_key_here
```

### 3. Launching EverMemOS
In a separate terminal, start the episodic memory vector database layer:
```bash
uv run python src/run.py
```

### 4. Booting EverTutor
In your active terminal, ensure your dependencies (`streamlit`, `python-dotenv`, `openai`) are installed, and launch the frontend:
```bash
streamlit run ever_tutor/app.py
```

---

## 📺 Video Demo

![EverTutor Demo](demo.mp4)
https://youtu.be/U4PoIztb4zg
*(Note: If the embedded video does not play in your environment, please download the `demo.mp4` file located in the root of this repository to watch locally).*
