"""
RAG Project Template (OpenRouter + OpenAI Embeddings)

NOTE:
This is a production-ready template based on your project structure.
Replace YOUR_OPENROUTER_API_KEY and pdf_folder before running.
"""

import os
import re
import time
import pickle
import faiss
import numpy as np
import pandas as pd
from typing import List, Optional
from openai import OpenAI
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import requests
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
class RAGProject:
    def __init__(self, pdf_folder:str,
                 api_key:str=API_KEY,
                 model:str="openai/gpt-4.1-mini",
                 embedding_model:str="text-embedding-3-small",
                 base_url:str="https://openrouter.ai/api/v1"):

        self.pdf_folder = pdf_folder
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.embedding_model = embedding_model
        self.index_path="faiss_openrouter_index.idx"
        self.docs_path="faiss_openrouter_docs.pkl"

    def clean(self,text):
        text=re.sub(r"\s+"," ",text)
        return text.strip()

    def load_documents(self):
        docs=[]
        for f in os.listdir(self.pdf_folder):
            if f.lower().endswith(".pdf"):
                docs.extend(PyPDFLoader(os.path.join(self.pdf_folder,f)).load())
        return docs

    def prepare_index(self):
        docs=self.load_documents()
        splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
        chunks=[]
        for d in docs:
            chunks.extend(splitter.split_text(self.clean(d.page_content)))

        rec_docs=[Document(page_content=c) for c in chunks]

        embeddings=[]
        batch_size=20
        for i in range(0,len(rec_docs),batch_size):
            batch=[d.page_content for d in rec_docs[i:i+batch_size]]
            resp=self.client.embeddings.create(
                model=self.embedding_model,
                input=batch
            )
            embeddings.extend([x.embedding for x in resp.data])
            time.sleep(2)

        emb=np.array(embeddings,dtype=np.float32)

        index=faiss.IndexFlatL2(emb.shape[1])
        index.add(emb)

        faiss.write_index(index,self.index_path)
        with open(self.docs_path,"wb") as f:
            pickle.dump(rec_docs,f)

    def load_index(self):
        self.index=faiss.read_index(self.index_path)
        with open(self.docs_path,"rb") as f:
            self.docs=pickle.load(f)

    def embed_query(self,q):
        r=self.client.embeddings.create(
            model=self.embedding_model,
            input=q
        )
        return np.array(r.data[0].embedding,dtype=np.float32)

    def retrieve(self,q,k=5):
        e=self.embed_query(q)
        if len(e)!=self.index.d:
            raise ValueError(f"Embedding dimension mismatch: {len(e)} vs {self.index.d}")
        D,I=self.index.search(e.reshape(1,-1),k)
        return [self.docs[i] for i in I[0]]

    def prompt(self,context,question):
        return f"""
Answer ONLY from the retrieved context.

If the answer is not explicitly present, reply exactly:

The provided documents do not contain enough information to answer this question.

Context:
{context}

Question:
{question}
"""

    def ask(self,question,k=5):
        docs=self.retrieve(question,k)
        context="\n\n".join(d.page_content for d in docs)

        r=self.client.chat.completions.create(
            model=self.model,
            messages=[{"role":"user","content":self.prompt(context,question)}],
            temperature=0.1,
            max_tokens=500
        )
        return r.choices[0].message.content

if __name__=="__main__":
    pdf_folder="data"
    rag=RAGProject(pdf_folder)
    if not os.path.exists("faiss_openrouter_index.idx"):
        rag.prepare_index()
    rag.load_index()
    print(rag.ask(input("Enter your question: ")))
