def circuit_breaker(func):
    def breaker(*args, **kwargs):
        print("Going to call function")
        func(*args, **kwargs)
        print("Function called")

    return breaker
