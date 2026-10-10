from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from django.conf import settings
import os
load_dotenv()

def create_Database(pdf_file):


   pdf_folder = os.path.join(
        settings.MEDIA_ROOT,
        "pdf"
    )

   os.makedirs(
        pdf_folder,
        exist_ok=True
    )

   pdf_path = os.path.join(
        pdf_folder,
        pdf_file.name
    )

   with open(pdf_path, "wb+") as destination:

        for chunk in pdf_file.chunks():

            destination.write(chunk)



###load the pdf
   load_pdf = PyPDFLoader(pdf_path)
   docs = load_pdf.load()


  #embeddigs
   embedding = MistralAIEmbeddings(
    model="mistral-embed",

  )

   if not docs:
     raise Exception("No text could be extracted from the PDF.")


  ####chunks ->spliting
   Chunks = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
  )
   text = Chunks.split_documents(docs)

   chroma_path = os.path.join(
        settings.BASE_DIR,
        "chroma_db"
    )

   print("Chroma database:", chroma_path)

  ###vector data base

   data  = Chroma(
    embedding_function=embedding,
    collection_name="pdf_documents",
    persist_directory="chroma_db"
  )


   ##daed chunks
   data.add_documents(text)

   return data
