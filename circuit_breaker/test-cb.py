import time

from circuit_breaker import *
import requests

@circuit_breaker_decorator
def sleep_call():
    time.sleep(3)
    print('sleep done!')

@circuit_breaker_decorator
def ext_call(num):
    '''url = 'http://google.com'
    response = requests.get(url)
    print(response.status_code)
    print(response.content)'''
    return 2 / num


#cb_obj = CircuitBreaker()

def test_with_exception_failure():
    try:
        print(ext_call(0))
    except:
        print('caught exception call1')
    finally:
        print()

    try:
        print(ext_call(0))
    except:
        print('caught exception call2')
    finally:
        print()

    try:
        print('call3 - open')
        print(ext_call(0))
    except:
        print('caught exception call3 - open')
    finally:
        print()

    try:
        print('call4 - open')
        print(ext_call(0))
    except:
        print('caught exception call4 - open')
    finally:
        print()

    print('sleep 4 seconds')
    time.sleep(4)

    # half open to open
    '''try:
        print(ext_call(0))
    except:
        print('caught exception call5 - half open')
    finally:
        print()'''

    # half open to closed
    print('call 6 - success call')
    print(ext_call(2))


def test_with_timeout_failure():
    try:
        print(sleep_call())
    except:
        print('caught exception call1')
    finally:
        print()

    try:
        print(sleep_call())
    except:
        print('caught exception call2')
    finally:
        print()

    try:
        print('call3 - open')
        print(sleep_call())
    except:
        print('caught exception call3 - open')
    finally:
        print()

    try:
        print('call4 - open')
        print(sleep_call())
    except:
        print('caught exception call4 - open')
    finally:
        print()

    print('sleep 4 seconds')
    time.sleep(4)

    # half open to open
    '''try:
        print(sleep_call(0))
    except:
        print('caught exception call5 - half open')
    finally:
        print()'''

    # half open to closed
    print('call 6 - success call')
    print(sleep_call())



print('testing cb')
print()

print(ext_call(2))
print()
'''print(ext_call(3))
print()
print(ext_call(4))
print()'''

#test_with_exception_failure()
test_with_timeout_failure()
