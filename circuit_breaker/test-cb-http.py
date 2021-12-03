from circuit_breaker import *
import requests
import time

@circuit_breaker_decorator
def ext_call(url):
    return requests.get(url)


url_ok = 'http://google.com'
url_fail = 'http://localhost:5000'

def test_with_failure():
    try:
        print(ext_call(url_fail))
    except:
        print('caught exception call1')
    finally:
        print()

    try:
        print(ext_call(url_fail))
    except:
        print('caught exception call2')
    finally:
        print()

    try:
        print('call3 - open')
        print(ext_call(url_fail))
    except CircuitBreakerException as e:
        print('Caught CircuitBreaker exception: ', e)
    except:
        print('caught exception call3 - open')
    finally:
        print()

    try:
        print('call4 - open')
        print(ext_call(url_fail))
    except CircuitBreakerException as e:
        print('Caught CircuitBreaker exception: ', e)
        print("{0}".format(e))
    except:
        print('caught exception call4 - open')
    finally:
        print()

    print('sleep 4 seconds')
    time.sleep(4)

    # half open to open
    try:
        print(ext_call(url_fail))
    except CircuitBreakerException as e:
        print(e)
        print("{0}".format(e))
    except:
        print('caught exception call5 - half open')
    finally:
        print()

    # half open to closed
    '''print('call 6 - success call')
    print(ext_call(url_ok))'''


def test_with_success_and_failure():
    try:
        print(ext_call(url_fail))
    except:
        print('caught exception call1')
    finally:
        print()

    print('call2 - success')
    print(ext_call(url_ok))
    print()

    try:
        print(ext_call(url_fail))
    except:
        print('caught exception call3')
    finally:
        print()


print('testing cb')
print()
print(ext_call(url_ok))
print()
test_with_failure()

# tests if state goes back to closed after one success response and failure count is reset to zero
#test_with_success_and_failure()