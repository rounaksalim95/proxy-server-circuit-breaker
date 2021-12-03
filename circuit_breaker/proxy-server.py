from flask import Flask, request, Response, jsonify
import requests

# import circuit_breaker
from circuit_breaker import *

app = Flask(__name__)


''''@app.route('/success')
@circuit_breaker_decorator
def proxy_test_success(*args, **kwargs):
    # print(request.url)

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, 'http://127.0.0.1:4000/'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response

@app.route('/failure')
@circuit_breaker_decorator
def proxy_test_failure(*args, **kwargs):
    # print(request.url)

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, 'http://127.0.0.1:5000/'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response
'''
@app.route('/test/<req_type>')
@circuit_breaker_decorator
def proxy_test(req_type):
    # print(request.url)
    port_num = 5000
    if req_type == 'success':
        port_num = 4000
    elif req_type == 'failure2':
        port_num = 6000

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, 'http://127.0.0.1:%s/'%port_num),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response


@app.errorhandler(Exception)
def generic_error(error):
    # for x in CircuitBreakerMonitor.get_circuits():
    #     msg = "{} circuit state: {}. Time till open: {}"
    #     print(msg.format(x.name, x.state, x.open_remaining))
    # return {"Error": msg.format(x.name, x.state, x.open_remaining)}
    return {"Error": str(error)}



if (__name__ == "__main__"):
    app.run(host='127.0.0.1', port=3000, debug=True)