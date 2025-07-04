# 1. Python суурьтай image
FROM python:3.12-slim

# 2. Ажлын директори үүсгэх
WORKDIR /app

# 3. Requirements-ээ түрүүлж хуулах (кэшлэнэ)
COPY requirements.txt .

# 4. Flask болон бусад хамаарал суулгах
RUN pip install --no-cache-dir -r requirements.txt

# 5. Кодоо хуулах
COPY . .

# 6. Порт нээх
EXPOSE 5000

# 7. App ажиллуулах
CMD ["python3", "app.py"]
