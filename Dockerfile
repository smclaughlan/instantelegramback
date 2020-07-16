FROM python:3.8-buster

RUN apt-get update && apt-get install -y netcat

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
# EXPOSE 5000

CMD ["gunicorn", "app:app"]
