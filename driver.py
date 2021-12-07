import time

import requests

# from circuit_breaker.circuit_breaker import circuit


def call_api(url):
    response = requests.get(url)
    print(response.text)


call_api("http://127.0.0.1:3000/")
time.sleep(1)
call_api("http://127.0.0.1:3000/")
time.sleep(1)
call_api("http://127.0.0.1:3000/")
time.sleep(1)

call_api("http://127.0.0.1:3000/")
time.sleep(1)
call_api("http://127.0.0.1:3000/")
time.sleep(1)
call_api("http://127.0.0.1:3000/")
time.sleep(1)

print("start server")
time.sleep(10)
call_api("http://127.0.0.1:3000/")
# time.sleep(1)
call_api("http://127.0.0.1:3000/")
# time.sleep(1)
call_api("http://127.0.0.1:3000/")
# time.sleep(1)
