from functools import wraps
from datetime import timedelta, datetime

STATE_CLOSED = "CLOSED"
STATE_OPEN = "OPEN"
STATE_HALF_OPEN = "HALF_OPEN"


class CircuitBreaker(object):
    def __init__(self, name = None, max_failures=None, reset_timeout=None):
        self._name = name
        self._max_failures = max_failures
        self._reset_timeout = reset_timeout
        self._failure_count = 0
        self._state = STATE_CLOSED
        self._opened = datetime.utcnow()

    def __call__(self, wrapped_func):
        return self.decorate(wrapped_func)


    def decorate(self, function):
        self._name = function.__name__
        
        # CircuitBreakerManager.register(self)
        
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.call(function, *args, **kwargs)
        return wrapper

    def call(self, func, *args, **kwargs):
        """
        Calls the wrapped function and applies the circuit breaker to it.
        """
        
        if self.state == STATE_OPEN:
            print("STATE - OPEN", self.open_remaining)
            raise CircuitBreakerError(self)
        try:
            print("Calling wrapped function")
            result = func(*args, **kwargs)
        except Exception as e:
            self.__call_failed()
            raise

        self.__call_succeeded()
        return result



    def __call_succeeded(self):
        """
        Sets Circuit Breaker's state to CLOSED and resets failure_count
        """
        print("Call succeeded")
        self._state = STATE_CLOSED
        self._failure_count = 0

    def __call_failed(self):
        """
        Increments the failure count by 1 and switches state to OPEN if it is equal to max failures.
        """
        print("Call failed")
        self._failure_count += 1
        if(self._failure_count >= self._max_failures):
            self._state = STATE_OPEN
            self._opened = datetime.utcnow()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        if self._state == STATE_OPEN and self.open_remaining <= 0:
            return STATE_HALF_OPEN
        return self._state

    @property
    def failure_count(self):
        return self._failure_count

    @property
    def is_closed(self):
        return self.state == STATE_CLOSED
    
    @property
    def is_open(self):
        return self.state == STATE_OPEN

    @property
    def open_until(self):
        """
        The date and time when the circuit breaker will try to recover
        """
        return self._opened + timedelta(seconds=self._reset_timeout)

    @property
    def open_remaining(self):
        """
        Number of seconds remaining for ther circuit breaker to try recovery
        """
        return (self.open_until - datetime.utcnow()).total_seconds()


class CircuitBreakerError(Exception):
    def __init__(self, circuit_breaker, *args, **kwargs):
        super(CircuitBreakerError, self).__init__(*args, **kwargs)
        self._circuit_breaker = circuit_breaker

    def __str__(self, *args, **kwargs):
        return 'Circuit Breaker "%s" is in OPEN State until %s, FAILURES = %d, %d seconds remaining to try recovery' % (
            self._circuit_breaker.name,
            self._circuit_breaker.open_until, 
            self._circuit_breaker.failure_count,
            round(self._circuit_breaker.open_remaining)
            )


def circuit(max_failures=None,
            reset_timeout=None,
            name = None,
            cls=CircuitBreaker):

    if callable(max_failures):
        return cls().decorate(max_failures)
    else:
        return cls(max_failures = max_failures, reset_timeout = reset_timeout, name = name)



