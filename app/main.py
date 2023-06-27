from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

class TextData(BaseModel):
    text: str

def search_duckduckgo(text):
    url = "https://api.duckduckgo.com/?q={}&format=json".format(text)
    response = requests.get(url)
    data = response.json()

    # Attempt to get first related topic
    try:
        return data['RelatedTopics'][0]['Text']
    except IndexError:
        return "No result found"

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
def process_text(data: TextData):
    original_text = data.text
    duckduckgo_search = search_duckduckgo(original_text)
    upper_case_text = original_text.upper()
    text_length = len(original_text)

    return {"duckduckgo_search": duckduckgo_search, "upper_case": upper_case_text, "length": text_length}
