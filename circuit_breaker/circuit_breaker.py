from functools import update_wrapper
from datetime import datetime, timedelta

# TODO move this into CB class?
STATE_CLOSED = "CLOSED"
STATE_OPEN = "OPEN"
STATE_HALF_OPEN = "HALF_OPEN"

class CircuitBreaker:
    def __init__(self, max_failures=2, call_timeout=2, reset_timeout=3):
        self._max_failures = max_failures
        self._call_timeout = call_timeout
        self._reset_timeout = reset_timeout
        self._failures = 0
        self._state = STATE_CLOSED
        self.opened_at_datetime = None
        self.called_at_datetime = None

# TODO decide logic to update self._failures - for every success response, decrement or reset to zero? => reset to zero
    def decorate(self, func, *args, **kwargs):
        print('inside cb decorate')
        # if CB in open state, check if you should fail fast or move to half open
        if self._state == STATE_OPEN:
            # if current time < opened_at + reset_timeout => fail fast
            print('in open state check')
            cur_time = datetime.utcnow()    # TODO remove cur_time variable
            print('cur time ', cur_time)
            print('opened at ', self.opened_at_datetime)
            print('elapse time ', self.opened_at_datetime + timedelta(seconds=self._reset_timeout))
            if cur_time < (self.opened_at_datetime + timedelta(seconds=self._reset_timeout)):
                # TODO return http fail code
                return "request failed fast by CB"
            self._state = STATE_HALF_OPEN
        # calling the decorated function
        with self:
            print('running decorated function')
            self.called_at_datetime = datetime.utcnow()
            return func(*args, **kwargs)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        print('insideeee __exit__')
        #print(exc_type)
        response_time = datetime.utcnow() - self.called_at_datetime
        # if exception or timeout failure:
        if exc_type is not None or response_time > timedelta(seconds=self._call_timeout):
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