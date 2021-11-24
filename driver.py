import time

import requests

from circuit_breaker.circuit_breaker import CircuitBreaker


@CircuitBreaker()
def call_api(url):
    response = requests.get(url)
    print(response.json())


call_api("http://127.0.0.1:5000/test")
call_api("http://127.0.0.1:5000/test")
time.sleep(5)
call_api("http://127.0.0.1:5000/test")
call_api("http://127.0.0.1:5000/test")
call_api("http://127.0.0.1:5000/test")
call_api("http://127.0.0.1:5000/test")
