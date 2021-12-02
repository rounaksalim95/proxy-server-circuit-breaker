from functools import update_wrapper
from datetime import datetime, timedelta

STATE_CLOSED = "CLOSED"
STATE_OPEN = "OPEN"
STATE_HALF_OPEN = "HALF_OPEN"
HTTP_ERROR_CODES = [500, 503, 504]

class CircuitBreaker:
    def __init__(self, max_failures=2, call_timeout=2, reset_timeout=3):
        self._max_failures = max_failures
        self._call_timeout = call_timeout
        self._reset_timeout = reset_timeout
        self._failures = 0
        self._state = STATE_CLOSED
        self.opened_at_datetime = None
        self.called_at_datetime = None
        self.http_error_response_status_code = None

# decide logic to update self._failures - for every success response, decrement or reset to zero? => reset to zero
    def decorate(self, func, *args, **kwargs):
        print('inside cb decorate')
        # if CB in open state, check if you should fail fast or move to half open
        if self._state == STATE_OPEN:
            # if current time < opened_at + reset_timeout => fail fast
            print('in open state check')
            cur_time = datetime.utcnow()
            print('cur time ', cur_time)
            print('opened at ', self.opened_at_datetime)
            print('elapse time ', self.opened_at_datetime + timedelta(seconds=self._reset_timeout))
            if cur_time < (self.opened_at_datetime + timedelta(seconds=self._reset_timeout)):
                # TODO return http fail code
                return "Request failed fast by CB"
            self._state = STATE_HALF_OPEN
        # calling the decorated function
        with self:
            print('running decorated function')
            self.called_at_datetime = datetime.utcnow()
            #return func(*args, **kwargs)
            # if status code of response is in list HTTP_ERROR_CODES, then its a failure. So call __exit__
            response = func(*args, **kwargs)
            if response.status_code not in HTTP_ERROR_CODES:
                return response
            self.http_error_response_status_code = response.status_code

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        print('inside __exit__')
        #print(exc_type)
        response_time = datetime.utcnow() - self.called_at_datetime
        # if exception or timeout failure:
        if exc_type is not None or response_time > timedelta(seconds=self._call_timeout) or self.http_error_response_status_code:
            if self._state == STATE_CLOSED:
                self._failures += 1
                print('failure count  ', self._failures)
                if self._failures == self._max_failures:
                    self._state = STATE_OPEN
                    self.opened_at_datetime = datetime.utcnow()
                    print('max failures exceeded, state: ', self._state)
            elif self._state == STATE_HALF_OPEN:
                self._state = STATE_OPEN
                self.opened_at_datetime = datetime.utcnow()
                print('updated state to : ', self._state)
            self.http_error_response_status_code = None
        else:
            if self._state == STATE_HALF_OPEN:
                self._state = STATE_CLOSED
            self._failures = 0


def circuit_breaker_decorator(func):
    cb_obj = CircuitBreaker()

    def wrapper(*args, **kwargs):
        return cb_obj.decorate(func, *args, **kwargs)
    # return decorated function
    return wrapper