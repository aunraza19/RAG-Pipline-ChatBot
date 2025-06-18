# University Academic Policy Chatbot
## A RAG Pipline ChatBot
This project provides an intelligent chatbot designed to help university students quickly find answers to their academic policy questions. Leveraging Retrieval-Augmented Generation (RAG), the chatbot provides accurate, context-aware responses by searching through the university's academic manual.

## 📚 Project Overview:
Navigating dense academic manuals can be time-consuming and frustrating for students. This chatbot aims to solve that problem by offering an intuitive, conversational interface where students can simply ask questions in natural language and receive precise answers directly extracted from the official policy documents.

## 💡 Problem & Solution:
### The Problem:
University academic manuals are often lengthy, complex, and difficult to navigate. Students frequently struggle to find specific policies related to course withdrawal, grading, readmission, or other academic procedures, leading to confusion, delays, and reliance on administrative staff for basic queries.

### The Solution:
This chatbot utilizes a Retrieval-Augmented Generation (RAG) system to bridge the gap between complex documentation and student needs.

## Data Ingestion: The academic manual (a PDF document) is processed, split into manageable chunks, and converted into numerical representations called embeddings. These embeddings are stored in a ChromaDB vector store.
Information Retrieval: When a student asks a question, the chatbot converts the query into an embedding and searches the ChromaDB for the most relevant policy chunks.
Answer Generation: The retrieved policy chunks are then provided as context to a powerful Large Language Model (LLM) from Groq. The LLM uses this context to generate a concise and accurate answer, ensuring responses are grounded in the official academic policies.
User Interface: A user-friendly interface built with Streamlit allows students to easily interact with the chatbot, ask questions, and view the generated answers along with their original sources.
This system ensures that answers are not only conversational but also verifiable and directly linked to the official documentation, reducing ambiguity and improving student support.

## ✨ Features
Intelligent Q&amp;A: Answers student questions based on the provided academic manual.
Context-Aware Responses: Utilizes RAG to ensure answers are factual and sourced from relevant policy documents.
Source Attribution: Provides snippets and page numbers from the source document for transparency and verification.
User-Friendly Interface: Built with Streamlit for a simple and intuitive conversational experience.
Groq LLM Integration: Leverages the high-speed and efficient Groq API for rapid answer generation.
BAAI/bge-small-en-v1.5 Embeddings: Uses a high-quality open-source embedding model for effective semantic search.

## 🛠️ Tech Stack:

| Component         | Technology Used                    |
|------------------|-------------------------------------|
| LLM               | `Groq (llama3-8b-8192)`             |
| Embedding Model   | `BAAI/bge-small-en-v1.5` via `HuggingFaceEmbeddings` |
| Vector Store      | `ChromaDB`                          |
| PDF Parsing       | `PyPDFLoader` from `langchain-community` |
| Web Interface     | `Streamlit`                         |
| Backend Framework | `LangChain`                         |
| Configuration     | `.env` + `config.py`                |

---

## 📁 Project Structure:
```
rag_chatbot_project/
│
├── .env # Contains API keys (GROQ_API_KEY)
├── app.py # Streamlit-based frontend and UI logic
├── ingest.py # PDF parsing, chunking, embedding, and storing in vector DB
├── utils.py # Embedding, vector store, and LLM utilities
├── config.py # Centralized configuration constants
├── requirements.txt # Python package dependencies
├── academic_manual.pdf # University manual to query from
└── chroma_db/ # Directory to persist vector store
```
## 🚀 Getting Started:
Follow these steps to set up and run the Academic Policy Chatbot locally.

## Prerequisites:
Python 3.8+
pip (Python package installer)

## Installation:
### Clone the repository:

```Bash

git clone https://github.com/aunraza19/RAG-Pipline-ChatBot.git
cd your_repository_name
```
```bash
pip install -r requirements.txt
```

## Configuration:
Get your API Key:

Sign up for an account on Groq.
Generate an API key from your Groq console.
Create a .env file:
In the root directory of your project, create a file named .env and add your API key:

GROQ_API_KEY="gsk_YOUR_GROQ_API_KEY_HERE"
 HUGGINGFACEHUB_API_TOKEN="hf_YOUR_HF_TOKEN_HERE"  Optional: Only if your embedding model requires a Hugging Face token
Important: Do NOT commit your .env file to Git! It's included in .gitignore.

 ## Data Ingestion:
You need to process your academic_manual.pdf and build the vector database.

Place your PDF: Ensure your university's academic manual is named academic_manual.pdf and placed in the root directory of the project.
Run the ingestion script:
Bash

python ingest.py:
This script will load the PDF, split it into chunks, generate embeddings, and store them in the ./chroma_db directory. You will see progress messages in the console.
Run the Streamlit Chatbot
Once the data ingestion is complete, you can start the chatbot.

```Bash

streamlit run app.py
This will launch the Streamlit application in your web browser, typically at http://localhost:8501.
```


📈 Future Improvements:
Multi-Turn Conversation: Implement chat history using LangChain's ConversationalRetrievalChain for a more natural interaction.
Streaming Responses: Stream LLM output token by token for a faster perceived response time.
Enhanced Source Display: Use st.expander to neatly present sources and potentially highlight relevant snippets.
User Feedback: Add a mechanism (e.g., thumbs up/down buttons) to collect feedback on response quality, aiding in continuous improvement.
Hybrid Search/Re-ranking: Explore advanced retrieval techniques to enhance answer accuracy for complex queries.
