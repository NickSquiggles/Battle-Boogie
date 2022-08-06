FROM python:slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/logic.py src/main.py .

EXPOSE 8080
CMD ["python", "main.py"]

