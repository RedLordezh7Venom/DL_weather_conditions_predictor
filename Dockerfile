# Use an official Python runtime as a parent image
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#Copy rest of the application
COPY . .

EXPOSE 8501

CMD ["streamlit","run","app.py"]
