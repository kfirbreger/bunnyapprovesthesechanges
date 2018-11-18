FROM python:2-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt


