FROM python:3.11-slim-bullseye
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY app/ /code/app/
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]