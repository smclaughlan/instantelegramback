FROM python:3.8-buster

RUN apt-get update && apt-get install -y netcat

WORKDIR /app

COPY . .

RUN pip install pipenv && pipenv install

EXPOSE 5000

CMD ["pipenv", "run", "flask", "run"]
