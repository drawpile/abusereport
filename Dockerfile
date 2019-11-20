FROM python:3.7-alpine3.9

RUN adduser -D -u 1000 python
WORKDIR /home/python

COPY freeze.txt .
RUN pip install -r freeze.txt

COPY report_relay report_relay
USER python
CMD ["gunicorn", "report_relay.main:app", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker"]

