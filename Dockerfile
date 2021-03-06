# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-alpine

EXPOSE 8080

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "index.py"]