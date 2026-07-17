FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python", "f1_agent.py"]
# Force rebuild Wed May  6 01:01:53 PDT 2026
