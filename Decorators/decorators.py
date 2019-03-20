#!/usr/bin/env/python3


#1# - function decorator
from timeit import default_timer as timer
def my_decorator(function):
    def wrapped(*args, **kwargs):
        start = timer()
        function(*args, **kwargs)
        end = timer()
        print('Execution time: {}'.format(end-start))
    return wrapped

@my_decorator
def heavy_computation(steps=1000):
    result = 0
    for i in range(steps):
        result *= i*i/(i+1)*(i+2)*(i-1)*(i/(i+1))


#2# - parametrizing decorators
def repeat(number=10):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(number):
                result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(1)
def debug():
    print('debug!')

def deb():
    print('deb!')

foo = repeat(3)


#3# - functools wraps
from functools import wraps

def preserving_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        """Wrapped function docs"""
        return func(*args, **kwargs)
    return wrapped

@preserving_decorator
def func_with_docstring(params):
    """My turbo important docstring""" 
    print(params)


#4# caching decorator
import time
import hashlib
import pickle

cache = {}

def is_already_invalid(entry, duration):
    return (time.time() - entry['time']) > duration

def compute_cache_key(func, args, kwargs):
    key = pickle.dumps((func.__name__, args, kwargs))
    return hashlib.sha1(key).hexdigest()

def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kwargs):
            key = compute_cache_key(function, args, kwargs)
            
            # Does the key exist already ?
            if key in cache and not is_already_invalid(cache[key], duration):
                print("Key: {} already exists in cache".format(key))
                return cache[key]['value']
            
            # Computing
            result = function(*args, **kwargs)
            print("Key: {} did not exist in cache!".format(key))
            cache[key] = {
                'value': result,
                'time': time.time()
            }
            return result
        return __memoize
    return _memoize

@memoize()
def complex_computations(*args):
    return sum(args)


#4# proxy
class User():
    def __init__(self, roles):
        self.roles = roles

class Unauthorized(Exception):
    pass

def login(role):
    def _login(function):
        def __login(*args, **kwargs):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("Access forbidden!")
            return function(*args, **kwargs)
        return __login
    return _login

class LoginPage():
    @login('admin')
    def main_page(self):
        print("Hello, you have logged in succsfully!")









###################### main ####################
if __name__ == '__main__':


##1# - function decorator
    heavy_comp = my_decorator(lambda x: print(x*x*x*x))
    heavy_comp(1000000)
    heavy_computation(1000000)

##2# - parametrizing decorators
    debug()
    foo(deb)()

##3# - functools wraps
    func_with_docstring("FUNC WITH WRAPS")
    # remove @wraps(func) from preserving_decorator
    print(func_with_docstring.__name__)
    print(func_with_docstring.__doc__) 

##4# caching decorator
    import random as rnd
    for _ in range(20):
        complex_computations(rnd.randint(0, 10))

##5# proxy
    try:
        user = User(('user', 'tester'))
        web_page = LoginPage()
        web_page.main_page()
    except Exception as e:
        print(str(e))

    try:
        user = User(('admin', 'tester'))
        web_page.main_page()
    except Exception as e:
        print(str(e))