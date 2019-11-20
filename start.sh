# production style:
#gunicorn report_relay.main:App --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker

# dev server style:
python3 -m report_relay.main
