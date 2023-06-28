FROM python:3.11
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]