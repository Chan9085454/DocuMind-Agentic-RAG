# 🧠 DocuMind AI — Agentic RAG Chatbot for Multi-Format Document QA
Built an Agentic Retrieval-Augmented Generation (RAG) chatbot for multi-format document question answering using LangChain, ChromaDB, and Ollama, implementing an agent-based architecture (Planner, Retrieval, Reasoning, and Response Agents) for intelligent document understanding, semantic retrieval, and context-aware response generation.

## 🚀 Features
### 📂 Multi-Format Document Support
Upload and process:

- PDF
- DOCX
- TXT
- CSV

### 🤖 Agentic AI Architecture
Implements specialized agents for intelligent orchestration:

- **PlannerAgent** → Determines query execution strategy
- **RetrievalAgent** → Retrieves relevant document chunks
- **ReasoningAgent** → Performs context-aware reasoning
- **ResponseAgent** → Generates grounded responses
- **ToolAgent** → Handles external tools/utilities

### 🔍 Retrieval-Augmented Generation (RAG)
- Semantic search using embeddings
- Context-aware retrieval
- Document-grounded responses
- Reduced hallucinations

### 🧠 LLM-Powered Reasoning
- Local LLM integration using **Ollama**
- Context-based answer generation
- Extractive prompting for faithful document responses

### ⚡ FastAPI Backend
- High-performance API handling
- Upload and chat endpoints
- Scalable architecture

### 🎨 Streamlit UI
Interactive frontend for:

- File uploads
- Chat interface
- Response visualization

## 🏗️ System Architecture

   text
User Query
     │
     ▼
PlannerAgent
     │
     ▼
RetrievalAgent ───► Chroma Vector DB
     │
     ▼
ReasoningAgent
     │
     ▼
ResponseAgent
     │
     ▼
Final Answer

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- LangChain

### LLM
- Ollama
- phi3:mini

### Vector Database
- ChromaDB

### Embeddings
- Sentence Transformers

### Frontend
- Streamlit

### Document Processing
- PyMuPDF
- python-docx
- pandas

## 📁 Project Structure
DocuMind-AI/
│── app/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── reasoning_agent.py
│   │   ├── response_agent.py
│   │   └── tool_agent.py
│   │
│   ├── api/
│   │   ├── upload.py
│   │   └── chat.py
│   │
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   ├── chunker.py
│   │   └── embedder.py
│   │
│   ├── vectorstore/
│   │   └── chroma_store.py
│   │
│   ├── RAG/
│   │   └── llm_utils.py
│   │
│   └── main.py
│
│── UI/
│   └── streamlit_app.py
│
│── requirements.txt
│── README.md
│── .gitignore


## 🔄 Workflow
### Step 1: Upload Document
Document is parsed and chunked.

### Step 2: Embedding Generation
Chunks are converted into embeddings.

### Step 3: Vector Storage
Embeddings stored in **ChromaDB**.

### Step 4: Semantic Retrieval
Relevant chunks retrieved based on similarity.

### Step 5: Agentic Reasoning
Agents collaborate to generate response.

### Step 6: Final Response
Context-grounded answer returned to user.

## 🎯 Key Highlights
✅ Multi-format document support  
✅ Agentic AI workflow  
✅ Semantic search with ChromaDB  
✅ Local LLM support (Ollama)  
✅ FastAPI + Streamlit integration  
✅ Context-aware question answering  
✅ Reduced hallucination via RAG

## 📌 Future Improvements
- Multi-user authentication
- Chat history memory
- Conversation summarization
- Multi-document comparison
- Cloud deployment (AWS/GCP/Azure)
- Docker support
