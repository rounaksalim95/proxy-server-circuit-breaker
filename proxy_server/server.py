from flask import Flask, request, Response, jsonify
import requests

#import circuit_breaker
from circuit_breaker import circuit


app = Flask(__name__)




@app.route('/')
@circuit(max_failures=3, reset_timeout=6)
def proxy_test(*args, **kwargs):
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
    

@app.errorhandler(Exception)
def generic_error(error):
    # for x in CircuitBreakerMonitor.get_circuits(): 
    #     msg = "{} circuit state: {}. Time till open: {}"
    #     print(msg.format(x.name, x.state, x.open_remaining))
    # return {"Error": msg.format(x.name, x.state, x.open_remaining)}
    return{"Error": "Error"}

    

@app.route('/test/')
def _proxy3(*args, **kwargs):
    print(request.url)
    print(request.url.replace(request.host_url, 'http://127.0.0.1:5000/'))
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


if(__name__ == "__main__"):
    app.run(host='127.0.0.1', port=3000, debug=True)