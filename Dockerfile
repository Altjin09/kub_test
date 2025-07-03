# 1. Python суурьтай image ашиглана
FROM python:3.12-slim

# 2. Ажлын директори үүсгэх
WORKDIR /app

# 3. requirements.txt үүсгээгүй тул шууд бүх файлуудыг хуулна
COPY . /app

# 4. Flask суулгах
RUN pip install flask

# 5. Порт нээх
EXPOSE 5000

# 6. App ажиллуулах
CMD ["python", "app.py"]
