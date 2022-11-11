FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY /app .
COPY /app/start_prod.sh /

RUN apt-get update
RUN apt-get install -y cron
RUN pip install pip-tools
RUN pip-compile
RUN pip install -r requirements.txt

EXPOSE 8000
