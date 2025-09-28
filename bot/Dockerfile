FROM python:3.10-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .
ENV PYTHONPATH=/
CMD ["python", "main.py"]
