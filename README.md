# 🤖 AI PDF Chatbot

An AI-powered PDF chatbot that allows users to upload a PDF and ask questions about its content using Retrieval-Augmented Generation (RAG).

## 🚀 Features

- 📄 Upload and process PDF documents
- ✂️ Intelligent document chunking
- 🧠 Hugging Face sentence embeddings
- 🔎 FAISS vector similarity search
- 🔄 Conversational question rewriting
- 🤖 Qwen LLM for answer generation
- 💬 Interactive Gradio chatbot UI
- 🔐 Environment variables for API credentials
- 🚫 Answers are restricted to the uploaded PDF context

## 🛠️ Tech Stack

- Python
- Gradio
- LangChain
- Hugging Face
- Sentence Transformers
- FAISS
- Qwen
- PyPDF
- python-dotenv

## 🧠 RAG Architecture

```text
User Question
      ↓
Question Rewriting
      ↓
Query Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant PDF Chunks
      ↓
Qwen LLM
      ↓
Final Answer
