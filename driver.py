import requests

from circuit_breaker.circuit_breaker import circuit_breaker


@circuit_breaker
def call_api(url):
    response = requests.get(url)
    print(response.json())


call_api("http://127.0.0.1:5000/test")
