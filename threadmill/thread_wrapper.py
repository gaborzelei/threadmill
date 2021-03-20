from concurrent.futures.thread import ThreadPoolExecutor
from functools import wraps
from os import getenv
from typing import Callable

from .exceptions import ThreadExecutionWarning
from .singleton import Singleton


class ThreadWrapper(metaclass=Singleton):
    """ Singleton class for wrapping the new_thread decorator functionality """

    # Default number of max_workers is CPU count x5.
    # Specify MAX_WORKER_THREADS in the shell env to override this number.
    _THREAD_POOL = ThreadPoolExecutor(max_workers=getenv('MAX_WORKER_THREADS', default=None))

    def create_decorator(self, exception_handler: Callable = None):
        """
        Thread decorator factory to create a decorator instance.

        Args
            exception_handler:  An optional custom exception handler

        Notes
            When decorating a function, parentheses at the end of the decorator are required.
            - Do:    @new_thread()   -> Returns a decorator instance
            - Don't: @new_thread     -> Will decorate your function with a <Function> object that's useless in itself
        """
        def thread_decorator(wrapped_function):
            @wraps(wrapped_function)
            def dispatcher(*args, **kwargs):
                return self._THREAD_POOL.submit(
                    self._catcher,
                    wrapped_function,
                    exception_handler or self._default_handler,
                    *args,
                    **kwargs
                )
            return dispatcher
        return thread_decorator

    @staticmethod
    def _catcher(wrapped_function: Callable, exception_handler: Callable, *args, **kwargs):
        """
        Automatically catches and processes unhandled exceptions in a thread

        Args
            wrapped_function: The function the thread decorator is wrapping
            exception_handler: An exception handler method
            args: Positional arguments for the function the thread decorator has wrapped
            kwargs: Keyword arguments for the function the thread decorator has wrapped
        """
        try:
            return wrapped_function(*args, **kwargs)
        except Exception as ex:
            exception_handler(str(wrapped_function), ex, *args, **kwargs)
            return None

    @staticmethod
    def _default_handler(wrapped_function_name: str, ex: Exception, *args, **kwargs):
        """
        Default exception handler for the thread decorator

        Args
            ex: The exception to handle
            args: Positional arguments for the function the thread decorator has wrapped
            kwargs: Keyword arguments for the function the thread decorator has wrapped
        """
        raise ThreadExecutionWarning(
            'An exception occurred in thread {thread_name} {exception} (args: {args}, kwargs: {kwargs})'.format(
                thread_name=wrapped_function_name,
                exception=ex,
                args=args or None,
                kwargs=kwargs or None
            )
        )
