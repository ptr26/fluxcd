FROM python:3.9-slim

WORKDIR /app

COPY ./repositories/guest-book/src/db/requirements.txt .

RUN pip install -r requirements.txt

COPY ./repositories/guest-book/src/db/ .

CMD ["python", "app.py"]
