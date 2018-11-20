FROM alpine

EXPOSE 8000

RUN apk --update add uwsgi \
                    uwsgi-python3 \
                    python3

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

RUN pip3 install pipenv

COPY Pipfile* /
RUN pipenv install --three --system --deploy

RUN mkdir --p app/app

WORKDIR app
USER appuser

COPY app/* /app/app/
COPY bunnies.ini /app


CMD ["uwsgi", "--ini", "bunnies.ini"]
