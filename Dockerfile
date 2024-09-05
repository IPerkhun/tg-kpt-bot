FROM python:3.9-slim


WORKDIR /app

COPY . /app

COPY .env /app/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
