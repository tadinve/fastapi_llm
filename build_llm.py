import os
import pickle

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

loader = DirectoryLoader('./', glob='**/*.pdf')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
docsearch = FAISS.from_documents(texts, embeddings) 

file = open('model.pickle', 'wb')
pickle.dump(docsearch, file)

