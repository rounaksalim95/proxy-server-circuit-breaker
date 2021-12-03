import time

import requests
from circuit_breaker import *


# from circuit_breaker.circuit_breaker import circuit


def call_api(url):
    response = requests.get(url)
    print(response.text)


call_api("http://127.0.0.1:3000/test/success")
time.sleep(1)
call_api("http://127.0.0.1:3000/test/failure2")
time.sleep(1)
call_api("http://127.0.0.1:3000/test/failure2")
time.sleep(1)
call_api("http://127.0.0.1:3000/test/failure2")
time.sleep(1)

call_api("http://127.0.0.1:3000/test/failure2")
time.sleep(6)
# half open state
call_api("http://127.0.0.1:3000/test/failure2")
time.sleep(1)
# open state
time.sleep(6)
call_api("http://127.0.0.1:3000/test/success")
time.sleep(1)


