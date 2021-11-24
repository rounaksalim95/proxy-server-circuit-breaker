from functools import update_wrapper

STATE_CLOSED = "CLOSED"
STATE_OPEN = "OPEN"
STATE_HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self, max_failures=3, call_timeout=2, reset_timeout=60):
        self._max_failures = max_failures
        self._call_timeout = call_timeout
        self._reset_timeout = reset_timeout
        self._failures = 0
        self._state = STATE_CLOSED

    def __call__(self, func):
        update_wrapper(self, func)

        def wrapper(*args, **kwargs):
            if self._failures == self._max_failures:
                self._state = STATE_OPEN

            if self._state == STATE_CLOSED:
                print("Going to call function")
                try:
                    func(*args, **kwargs)
                    print("Function called")
                except Exception as e:
                    self._failures += 1
                    print("Excpetion while calling function: ", e)
            elif self._state == STATE_OPEN:
                print("Not calling function as circuit breaker is in open state")
            elif self._state == STATE_HALF_OPEN:
                print("Circuit breaker is in half open state")

        return wrapper
