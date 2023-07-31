from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from duckduckgo_search import DDGS
from itertools import islice
import asyncio
import concurrent.futures

import pickle
from langchain import OpenAI
from langchain.chains import RetrievalQA
import os
import openai
import time

openai.api_key = os.environ["OPENAI_API_KEY"]

file = open('app/models/model.pickle', 'rb')

llm = OpenAI(openai_api_key=openai.api_key)

docmodel = pickle.load(file)
def run_qa(q):
    start_time = time.time()
    print("LLM = ", q)
    qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=docmodel.as_retriever()
                                 )
    q = q + " give bullted answers where applicabele, also cite your source"
    print(f"Custom Model Time = {time.time()-start_time}")
    return qa.run(q)

def get_chatGPT_completion(model="text-davinci-003", prompt="print hello world!", temperature=0, max_tokens=256
                           ,  frequency_penalty=0.0,  presence_penalty=0.0):
    start_time = time.time()                           
    prompt = prompt + " also cite your source"
    print(prompt)
    response = openai.Completion.create( model=model,
                                        prompt=prompt,
                                        temperature=temperature,
                                        max_tokens=max_tokens,
                                        presence_penalty=presence_penalty,
                                        frequency_penalty=frequency_penalty,
                                        )
    resp = response.choices[0]["text"]
    print("response = ",resp)
    print(f"Chat GPT Time = {time.time()-start_time}")
    return resp

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

class TextData(BaseModel):
    text: str

def search_duckduckgo(text):
    # Attempt to get first related topic
    start_time = time.time()
    try:
        content = None
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(text, backend="lite")
            for r in islice(ddgs_gen, 1):
                content = r['body']
        print(f"Google Time = {time.time()-start_time}")
        return content
    except IndexError:
        return "No result found"


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
def process_text(data: TextData):
    original_text = data.text

    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(search_duckduckgo, original_text),
    #                executor.submit(run_qa, original_text),
    #                executor.submit(get_chatGPT_completion, prompt=original_text)]

    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # duckduckgo_search = results[0]
    # upper_case_text = results[1]
    # text_length = results[2]
    
    duckduckgo_search = search_duckduckgo(original_text)
    upper_case_text = run_qa(original_text)
    text_length = get_chatGPT_completion(prompt=original_text)

    return {"duckduckgo_search": duckduckgo_search, "upper_case": upper_case_text, 
            "length": text_length}
