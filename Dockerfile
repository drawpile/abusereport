FROM python:3-alpine

RUN adduser -D -u 1000 python
WORKDIR /home/python

RUN apk add gcc python3-dev musl-dev
COPY freeze.txt .
RUN pip install -r freeze.txt

COPY report_relay report_relay
USER python
CMD ["gunicorn", "report_relay.main:App", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker"]

