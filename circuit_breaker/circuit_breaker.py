# def circuit_breaker(func):
#     def breaker(*args, **kwargs):
#         print("Going to call function")
#         func(*args, **kwargs)
#         print("Function called")

#     return breaker

from functools import update_wrapper


class CircuitBreaker:
    def __init__(self, *args):
        for arg in args:
            print(arg)
        self.num_calls = 0

    def __call__(self, func):
        update_wrapper(self, func)

        def wrapper(*args, **kwargs):
            print("Going to call function")
            func(*args, **kwargs)
            print("Function called")

        return wrapper
