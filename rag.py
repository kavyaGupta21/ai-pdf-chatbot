import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
 


load_dotenv()

client=InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)
 


def load_pdf(pdf_path):
    loader=PyPDFLoader(pdf_path)
    documents=loader.load()
    print(f"Number of pages:{len(documents)}")
    return documents
    



#pdf into chunks
def split_documents(documents):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500
    )
    chunks=text_splitter.split_documents(documents)
    print(f"Number of chunks:{len(chunks)}")
    return chunks

#embedding model-text to vector
def create_vector_store(chunks):
    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("Embedding successfull")

    vector_store=FAISS.from_documents(
        chunks,
        embeddings
    )
    print("FAISS vector succcessfully created")
    return vector_store
 





# #k=3 means it finds 3 most relevant chunks
def retrieve_documents(vector_store, question):
    results = vector_store.similarity_search_with_score(
        question,
        k=5
    )
    if not results:
        return None

    return results

    # for result,score in results:
    #     print("Question:",question)
    #     print("Score:",score)

    # DISTANCE_THRESHOLD = 1.0

    # relevant_results = [
    #     (result, score)
    #     for result, score in results
    #     if score <= DISTANCE_THRESHOLD
    # ]

  




def generate_answer(question,relevant_results):
    context="\n\n".join(
        result.page_content
        for result,score in relevant_results
    )
    prompt=f"""
You are a helpful PDF assistant.

Answer the user's question using ONLY the context provided below.

IMPORTANT:
- If the answer is present in the context, answer it directly.
- If the answer is NOT present in the context, say exactly:
"I could not find the answer to your question in the PDF."
- Do not use outside knowledge.
Context:
{context}
Question:
{question}
Answer
    """
    response=client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
           { 
            "role":"user",
            "content":prompt
            }
        ]
    )
    return response.choices[0].message.content
def rewrite_question(question,history):
    if not history:
        return question

    conversation=""

    for item in history:
        conversation+=f"{item}\n"
    prompt=f"""
   You are a question rewriting assistant for a PDF question-answering system.

Your job is to rewrite the user's latest question into a complete,
standalone question that can be used for document retrieval.

IMPORTANT RULES:

1. Use the conversation history to understand words like:
   "it", "its", "they", "their", "this", "that", "these", and "those".

2. Preserve the exact topic being discussed.

3. Do NOT change the subject of the question.

4. If the user asks for an example of something mentioned in the
   previous conversation, keep that exact subject.

5. Return ONLY the rewritten question.

Conversation history:
{conversation}

Latest user question:
{question}
    """
    response=client.chat_completion(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    rewritten_question=response.choices[0].message.content.strip()
    return rewritten_question

def build_vector_store(pdf_path):
    documents=load_pdf(pdf_path)
    chunks=split_documents(documents)
    vector_store=create_vector_store(chunks)
    return vector_store

 