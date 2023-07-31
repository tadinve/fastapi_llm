python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.main:app --reload


#Docker
docker  build . -f Dockerfile --tag  fastapi
docker run -p 8001:8000  --env OPENAI_API_KEY=dsfdsfdsgdsg fastapi



