from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from django.conf import settings
load_dotenv()


models  = ChatGroq(
   model = "openai/gpt-oss-20b",
    temperature=0
)


embeddings = MistralAIEmbeddings(
    model="mistral-embed",
)

chroma_path = os.path.join( settings.BASE_DIR,
                            "chroma_db" )



vectorstore = Chroma(
  collection_name="pdf_documents",
  embedding_function= embeddings,
  persist_directory="chroma_db"
)


retrive_Data = vectorstore.as_retriever(
  search_type = "mmr",
  search_kwargs={
    "k":4,
    "fetch_k":10,
    "lambda_mult":0.5
  }
)



prompt = ChatPromptTemplate.from_messages(
  [
    ("system","""
    You are a PDF document assistant. 
    Answer the user's question ONLY using the information provided in the context. 
    Do not make up information. 
    If the answer cannot be found in the context, politely say: Sorry, I couldn't provide the answer from the uploaded document. Keep the answer clear and easy to understand.


"""),
(
  "human","""
Context:{context}
Question:{question}
"""
)
  ]
)

def get_input(user_input):

  docs = retrive_Data.invoke(user_input)
  context  = "\n".join(
    doc.page_content for doc in docs
  )
  
  final_prompt = prompt.invoke({"context":context,"question":user_input})

  response = models.invoke(final_prompt)
  print(response.content)

  return response.content

