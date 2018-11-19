FROM python:alpine

RUN apk --update add uwsgi
RUN pip install pipenv

COPY Pipfile* /
RUN pipenv install --system --deploy

RUN mkdir --p app/app

COPY bunnies.ini /app
COPY app/* app/app/

WORKDIR app

CMD ["uwsgi", "--ini", "bunnies.ini"]
