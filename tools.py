from operator import add
from typing import Any, Callable, Optional

#
#
# TYPES
#
#
# Used to indicate any operation that might raise an exception.
type Failable[T] = T | Exception

# Used to indicate code that has a side effect.
type SideEffect = Failable[None]

#
#
# FUNCTIONS
#
#
is_exception: Callable[[Any], bool] = lambda x: isinstance(x, Exception)
is_none: Callable[[Any], bool] = lambda x: x is None


def asserts(expression: Any) -> None:
    """
    Provides convenience so that assert keyword can be used in functions.
    """
    assert expression


def log[T, U](f: Callable[[T], U]) -> Callable[[T], U]:
    """
    Prints the name, input, and output of a function.
    """

    def _(arg):
        print(f"Function: {f.__name__}")
        print(f"Input: {arg}")
        result = f(arg)
        print(f"Output: {result}")
        return result

    return _


def map_opt[T](v: T) -> Optional[T]:
    """
    Maps a value to an optional value.
    """
    v if not is_none(v) else None


def map_fail[T](v: T) -> Failable[T]:
    """
    Maps a value to a failable value.
    """
    if not is_exception(v):
        return v
    else:
        return Exception(v)


def bind_opt[T, U](f: Callable[[T], U]) -> Callable[[Optional[T]], Optional[U]]:
    """
    Wraps the inputs and outputs of a function in an Optional tag so that continuation
    can be used. If an arg is None, None is returned so that they can continue to persist
    throughout a pipeline.
    """
    return lambda x: f(x) if x is not None else x


def bind_fail[T, U](f: Callable[[T], U]) -> Callable[[Failable[T]], Failable[U]]:
    """
    Wraps the inputs and outputs of a function in an Failable tag so that continuation
    can be used. If an arg is an Exception, it is returned so that they can continue to persist
    throughout a pipeline.
    """
    return lambda x: f(x) if not is_exception(x) else x  # type: ignore


#
#
# TESTS
#
#
if __name__ == "__main__":

    add_one: Callable[[int], int] = lambda x: x + 1
    tuplify: Callable[[int], tuple[int]] = lambda x: (x,)
    listify: Callable[[int], list[int]] = lambda x: [x]

    add_one_wlogging = log(add_one)

    add_one_wlogging(1)
    bind_opt(add_one_wlogging)(None)

