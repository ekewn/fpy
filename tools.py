from typing import Any, Callable, Optional

#
#
# TYPES
#
#
# Used to indicate any operation that might raise an exception.
type Failable[T] = T | Exception

# Used to indicate code that has a side effect. Implicitly failable.
type SideEffect = Failable[None]

#
#
# FUNCTIONS
#
#
is_exception: Callable[[Any], bool] = lambda x: isinstance(x, Exception)


def asserts(expression: Any) -> None:
    """
    Provides convenience so that assert keyword can be used in functions.
    """
    assert expression


def log(f: Callable) -> Callable:
    """
    Prints the name, input, and output of a function.
    """

    def _(*args, **kwargs):
        print(f"Function: {f.__name__}")
        print(f"Input: {args}")
        result = f(*args, **kwargs)
        print(f"Output: {result}")
        return result

    return _


def opt_map[T, U](f: Callable[[T], U]) -> Callable[[Optional[T]], Optional[U]]:
    """
    Wraps the inputs and outputs of a function in an Optional tag so that continuation
    can be used. If an arg is None, None is returned so that they can continue to persist
    throughout a pipeline.
    """
    return lambda x: f(x) if x is not None else x


def fail_map[T, U](f: Callable[[T], U]) -> Callable[[Failable[T]], Failable[U]]:
    """
    Wraps the inputs and outputs of a function in an Failable tag so that continuation
    can be used. If an arg is an Exception, it is returned is returned so that they can continue to persist
    throughout a pipeline.
    """
    return lambda x: f(x) if not is_exception(x) else x  # type: ignore


#
#
# TESTS
#
#
if __name__ == "__main__":

    def add_one(x: int) -> int:
        return x + 1

    def strang(x: int) -> str:
        return str(x)

    log(opt_map(add_one))(1)
    log(opt_map(add_one))(None)
    log(opt_map(strang))(2)
    log(opt_map(strang))(None)
    log(fail_map(add_one))(3)
    log(fail_map(add_one))(Exception("this isn't great"))
    log(fail_map(strang))(4)
    log(fail_map(strang))(Exception("asdfasd"))

