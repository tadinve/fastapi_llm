import pickle
from langchain import OpenAI
from langchain.chains import RetrievalQA
import os
import openai
from langchain.embeddings.openai import OpenAIEmbeddings


openai.api_key = os.environ["OPENAI_API_KEY"]

file = open('model.pickle', 'rb')

llm = OpenAI(openai_api_key=openai.api_key)

docmodel = pickle.load(file)
from my_lib import wrap_text
def run_qa(q):
    qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=docmodel.as_retriever()
                                 )
    q = q + " give bullted answers where applicabele, also cite your source"
    wrap_text(qa.run(q),numchars=120)

q1 = "How can I analyze historical performance data with BMC AMI Ops Monitor for Java Environments?"
print(q1)
run_qa(q1)