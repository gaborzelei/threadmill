# Wat

This is a small library to help with threading in `Python 3.6+`.
It contains a decorator function that makes it very easy to run a method or function in a new thread.

# Installation

Currently, this repo is not in pip - it may never get to that point, actually. 

You will need to install `wheel` for this to work:
```bash
pip install wheel
```

To install `threadmill` using `pip` run the following command:
```bash
pip install git+https://github.com/gaborzelei/threadmill
```

# How to use

A few examples can be found below. 
**Make sure not to omit the parentheses from the end of the decorator, otherwise you'll get an error.**

## Simple example
```python
from threadmill import new_thread

# Decorate your function with @new_thread()
@new_thread()
def my_awesome_function(positional_arg1: int, positional_arg2: str, keyword_arg: float = 1.234) -> int:
    # awesome shit happens here
    pass

# Call your function as you'd normally do. A handle object will be returned here.
# This operation is non-blocking, execution will not wait for your function to return here.
handle = my_awesome_function(1234, 'test', keyword_arg=5.678)

# Do some stuff here (optional)

# When it comes to the point where you need the return value of your function, 
# you can await it by calling handle.result(). This will block execution until
# your function returns and the thread finishes.
return_value_from_function = handle.result()
```

## Loop example
```python
from random import randint
from threadmill import new_thread

# Decorate your function with @new_thread()
@new_thread()
def my_awesome_function(positional_arg1: int, positional_arg2: str, keyword_arg: float = 1.234) -> int:
    # awesome shit happens here
    pass

# Set up a list for your handles
handles = []

# Start 10 threads. This will not block execution on the main thread
for i in range(10):
    handles.append(my_awesome_function(randint(0, i), 'test'))

# Do some stuff here (optional)

# Get results from threads. This bit is blocking the main thread
values = [handle.result() for handle in handles]
```

# Known issues and limitations
Type hinting is broken for `handle.result()`. 
This is a limitation that comes from the `futures` module and there's no known solution to it at this point in time.

Also, there are no unit tests, for which I'm genuinely ashamed...
