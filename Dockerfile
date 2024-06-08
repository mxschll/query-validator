FROM python:3.9-slim
RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY /validator /app/validator
RUN mkdir /app/queries

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

