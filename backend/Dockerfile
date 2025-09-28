FROM python:3.9-slim

WORKDIR .

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
