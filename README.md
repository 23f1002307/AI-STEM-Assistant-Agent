\# AI STEM Accessibility Assistant



An Agentic AI-powered web application designed to make STEM content accessible for visually impaired learners by converting images (graphs, diagrams, charts) into structured, screen-reader-friendly explanations with interactive reasoning and follow-up capabilities.



\---



\## 🚀 Problem Statement



STEM education heavily relies on visual elements such as graphs, diagrams, and charts. These are often inaccessible to visually impaired users because:



\- Screen readers cannot interpret images effectively

\- Existing AI tools provide generic descriptions instead of structured explanations

\- Lack of interactivity and context-aware learning



\---



\## 💡 Proposed Solution



This project introduces an \*\*Agentic AI system\*\* that:



\- Interprets STEM images using a multi-agent pipeline

\- Generates structured, accessible explanations

\- Allows users to interact with the system through follow-up questions

\- Incorporates \*\*Human-in-the-Loop (HITL)\*\* for improved accuracy and control

\- Supports \*\*feedback-driven retry loops\*\* for better interpretation



\---



\## 🎯 Key Features



\### 🤖 Multi-Agent System

The application uses multiple specialized agents:

\- Vision Agent → Extracts image description

\- Structure Agent → Converts into structured data

\- Reasoning Agent → Understands STEM concept

\- Accessibility Agent → Generates screen-reader-friendly output

\- Chat Agent → Handles follow-up questions



\---



\### 🔄 LangGraph Orchestration

\- Agents are orchestrated using \*\*LangGraph\*\*

\- Shared state enables collaboration between agents

\- Conditional routing enables dynamic workflows

\- Supports looping and adaptive execution



\---



\### 🧠 State Management

\- Each agent reads and updates a shared state

\- Ensures consistent reasoning across the pipeline

\- Maintains context across all agent interactions



\---



\### 💾 Persistent Memory

\- Stores full workflow state in `memory.json`

\- Enables context-aware follow-up questions

\- Maintains session continuity across requests



\---



\## 👤 Human-in-the-Loop (HITL)



The system introduces an interactive decision point after image interpretation:



\- ✅ \*\*Confirm\*\* → Continue processing normally  

\- ⏭ \*\*Skip\*\* → Continue without validation  

\- ❌ \*\*Reject\*\* → Trigger reprocessing  



This gives users control over AI decisions and improves trust in outputs.



\---



\## 🔁 Feedback Loop (Retry-Based HITL)



Unlike basic HITL systems that stop execution, this project implements a \*\*feedback-driven retry loop\*\*:



\### 🔄 Behavior:

Vision → HITL → Decision

↓

Reject → Vision AGAIN → HITL AGAIN

Copy



\### 🧠 What This Means:

\- The system \*\*does not terminate on rejection\*\*

\- Instead, it \*\*loops back to the Vision Agent\*\*

\- Generates a new interpretation of the same image

\- Allows iterative refinement without re-uploading



\### 🎯 Benefits:

\- Improves accuracy through repeated attempts

\- Mimics real human-AI collaboration

\- Eliminates friction of re-uploading images

\- Demonstrates true \*\*agentic feedback control\*\*



\---



\### 💬 Context-Aware Chat

\- Users can ask follow-up questions

\- Chat agent uses full workflow context

\- Provides deeper and more accurate explanations



\---



\### ♿ Accessibility-Focused Output

\- Generates clean HTML with headings, lists, and structure

\- Optimized for screen readers (NVDA, JAWS)

\- Avoids complex or noisy markup



\---



\## 🏗️ System Architecture

User Input (Image)

↓

LangGraph Workflow

↓

Vision Agent → HITL → (Feedback Loop if Rejected)

↓

Structure → Reasoning → Accessibility

↓

Final Output

↓

Persistent Memory

↓

Follow-up Questions (Chat Agent)

Copy



\---



\## ⚙️ How It Works



1\. User uploads an image

2\. Vision Agent analyzes the image

3\. System pauses for HITL decision

4\. Based on user input:

&#x20;  - Confirm / Skip → Continue pipeline

&#x20;  - Reject → Re-run Vision Agent (loop)

5\. Structured explanation is generated

6\. User can ask follow-up questions using full context



\---



\## 🛠️ Tech Stack



\### Backend

\- FastAPI

\- Python



\### AI \& Agent Framework

\- OpenAI GPT (gpt-4o-mini)

\- LangChain

\- LangGraph



\### Frontend

\- HTML

\- CSS

\- JavaScript



\### Storage

\- JSON-based persistent memory



\---



\## 👥 Who Will Benefit



\- Visually impaired students learning STEM

\- Educators teaching accessible content

\- Researchers working on AI accessibility

\- Developers exploring Agentic AI systems



\---



\## 🔥 Highlights



\- True \*\*Agentic AI system\*\* (not just an LLM app)

\- Real \*\*Human-in-the-Loop integration\*\*

\- \*\*Feedback-driven retry loop (advanced HITL)\*\*

\- \*\*Dynamic workflow routing\*\*

\- \*\*Persistent contextual memory\*\*

\- Accessibility-first design



\---



\## 🚀 Future Improvements



\- Voice output (text-to-speech)

\- Real-time streaming responses

\- Database-backed memory (Redis / Vector DB)

\- User correction-based HITL (not just retry)

\- Advanced diagram understanding models



\---



\## 📌 Conclusion



This project demonstrates how \*\*Agentic AI workflows can significantly improve accessibility in STEM education\*\*, enabling visually impaired users to interact with complex visual content in a structured, understandable, and interactive way.



The addition of \*\*feedback loops and HITL transforms the system from a static AI pipeline into an adaptive, interactive intelligence system.\*\*

