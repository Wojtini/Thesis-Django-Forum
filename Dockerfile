FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY / .

RUN pip install pip-tools
RUN pip-compile
RUN pip install -r requirements.txt

EXPOSE 8000


