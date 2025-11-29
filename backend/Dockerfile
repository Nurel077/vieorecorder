FROM python:3.10

WORKDIR /app

# Сначала копируем requirements.txt для кэширования
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем весь проект
COPY . .

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]