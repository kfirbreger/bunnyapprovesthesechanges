FROM alpine:3.20

EXPOSE 8000
# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN apk --update add --no-cache python3 py3-pip uwsgi uwsgi-python3

COPY requirements.txt /
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

RUN mkdir --p /app

WORKDIR /app
USER appuser

COPY app/* /app/
COPY bunnies.ini /app


CMD ["uwsgi", "--ini", "bunnies.ini"]
