FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Очень важно! Рабочая директория — там, где main.py
WORKDIR /app/backend

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
