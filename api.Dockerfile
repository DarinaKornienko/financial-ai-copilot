
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .


RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY api/ api/
COPY agents/ agents/
COPY rag/ rag/
COPY tools/ tools/

CMD ["python", "api/server.py"]