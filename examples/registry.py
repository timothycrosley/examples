from typing import Any, Callable

from examples.example import CallableExample


class ExampleRegistry:
    """An object that holds a set of examples as they are registered."""

    def __init__(self):
        self.examples = []

    def add_call(self, *args, **kwargs):
        def add_example_wrapper(function):
            self.examples.append(CallableExample(function, args=args, kwargs=kwargs))
            return function

        return add_example_wrapper

    def add_call_with_returns(self, _returns: Any, *args, **kwargs) -> Callable:
        def add_example_wrapper(function: Callable) -> Callable:
            self.examples.append(
                CallableExample(function, returns=_returns, args=args, kwargs=kwargs)
            )
            return function

        return add_example_wrapper

    def verify_signatures(self, verify_types: bool = True) -> None:
        for example in self.examples:
            example.verify_signature(verify_types=verify_types)
