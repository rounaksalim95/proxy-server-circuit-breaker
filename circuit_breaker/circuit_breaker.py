# def circuit_breaker(func):
#     def breaker(*args, **kwargs):
#         print("Going to call function")
#         func(*args, **kwargs)
#         print("Function called")

#     return breaker

from functools import update_wrapper

STATE_CLOSED = "CLOSED"
STATE_OPEN = "OPEN"
STATE_HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self):
        self._num_calls = 0
        self._state = STATE_CLOSED

    def __call__(self, func):
        update_wrapper(self, func)

        def wrapper(*args, **kwargs):
            if self._state == STATE_CLOSED:
                print("Going to call function")
                self._num_calls += 1
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    self._state = STATE_OPEN
                    print("Excpetion while calling function: ", e)
                print("Function called %s time/s" % self._num_calls)
            elif self._state == STATE_OPEN:
                print("Not calling function as circuit breaker is in open state")
            elif self._state == STATE_HALF_OPEN:
                print("Circuit breaker is in half open state")

        return wrapper
