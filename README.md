# Proxy Server Circuit Breaker

This circuit breaker is to be used specificially with HTTP servers.

## Circuit Breaker Pattern

![circuit-breaker](./images/circuit-breaker.png)

The circuit breaker pattern is used to avoid adding additional load on failing services.

It works like a traditional circuit breaker. When a service is down and the calls to it are either failing or timing out, the circuit breaker will trip/open. A max failure count threshold is used to determine when the circuit breaker should trip.

Every failed call or timeout (based on call timeout threshold) will increment the failure count. When the failure count crosses the max failure count then the circuit will trip and enter the `OPEN` state.

Any call made to the service while the circuit is open will result in the call not being made and a `CircuitBreakerOpenException` being thrown.  
After the configured reset timeout the circuit will enter the `HALF_OPEN` state. In this state the call a call to the service will be made and if it goes through then the circuit will enter the `CLOSED` state and reset the failure count.  
A failure in this state will cause the circuit breaker to trip again and enter the `OPEN` state.

## Implementation

We decided to implement the circuit breaker using a decorator class.

The `CircuitBreaker` decorator class is used to wrap the service call and maintains state of the circuit breaker. This state holds the configuration (max failure count, call timeout, reset timeout), state of the circuit breaker (OPEN, HALF_OPEN, CLOSED) and the failure count.

### Setup

- Run `pip3 install -r requirements.txt` to install the required dependencies
- Run `python3 server.py` to start the proxy server for testing purposes
- Run `python3 driver.py` to run the main file that makes use of the `CircuitBreaker` decorator

## Proxy Server

A proxy server is a server that sits in front of the individual services and routes the calls from the client to the services. This is a also known as a reverse proxy.

There are a couple of benefits of using a reverse proxy:

- It hides the IP addresses of the individual services
- It can help improve security
- It can help with load balancing
- It can help improve performance

In our use case of a circuit breaker specifically it makes sense to apply the circuit breaker to the proxy server instead of each individual client. This way the proxy server is directly able to trip the circuit breaker and avoid making calls to the inidividual services that are failing.
