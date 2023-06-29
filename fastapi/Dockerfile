FROM python:3.11-slim-bullseye

WORKDIR /llm

COPY ./requirements.txt /llm/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /llm/requirements.txt

COPY ./src /llm/src

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]