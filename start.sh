python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.main:app --reload
