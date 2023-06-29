from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from duckduckgo_search import DDGS
from itertools import islice


import pickle
from langchain import OpenAI
from langchain.chains import RetrievalQA
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

file = open(os.getcwd()+'/src/model/llm.pickle', 'rb')
llm = OpenAI(openai_api_key=openai.api_key)
docmodel = pickle.load(file)

def run_qa(q):
    qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=docmodel.as_retriever()
                                 )
    q = q + " give bullted answers where applicable, also cite your source"
    return qa.run(q)

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

class TextData(BaseModel):
    text: str

def search_duckduckgo(text):
    # Attempt to get first related topic
    try:
        content = None
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(text, backend="lite")
            for r in islice(ddgs_gen, 1):
                content = r['body']
        return content
    except IndexError:
        return "No result found"

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
def process_text(data: TextData):
    original_text = data.text
    duckduckgo_search = search_duckduckgo(original_text)
    upper_case_text = run_qa(original_text)
    text_length = len(original_text)

    return {"duckduckgo_search": duckduckgo_search, "upper_case": upper_case_text, 
            "length": text_length}



# with DDGS() as ddgs:
#     for r in ddgs.text('How can I analyze historical performance data with BMC AMI Ops Monitor for Java Environments?', region='wt-wt', safesearch='on', timelimit='y'):
#         print(r)            