from typing import Callable

from .thread_wrapper import ThreadWrapper


def new_thread(exception_handler: Callable = None):
    """
    Runs a method or function in a separate thread.

    Args
        exception_handler: An optional custom exception handler
                           Input parameters it will receive: function name, exception object, *args, **kwargs

    Notes
        When decorating a function, parentheses at the end of the decorator are required.
        - Do: @new_thread()
        - Don't: @new_thread
    """
    return ThreadWrapper().create_decorator(exception_handler)
