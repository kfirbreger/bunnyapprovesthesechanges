FROM python:alpine

EXPOSE 8000

RUN apk --update add uwsgi

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN pip install pipenv

COPY Pipfile* /
RUN pipenv install --system --deploy

RUN mkdir --p app/app

WORKDIR app
USER appuser

COPY bunnies.ini /app
COPY app/* app/app/


CMD ["uwsgi", "--ini", "bunnies.ini"]
