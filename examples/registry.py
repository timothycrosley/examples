from pydantic import create_model

import inspect
import typing


class NotDefined:
    pass


class Example:
    """Defines a single Example"""

    def __init__(self, callable_object, args, kwargs, returns=NotDefined):
        self.args = args
        self.kwargs = kwargs
        self.callable_object = callable_object
        self.returns = returns

    def verify_signature(self, verify_types=True):
        """Verifies that the example makes sense against the functions signature"""
        bound = inspect.signature(self.callable_object).bind(self.args, self.kwargs)

        annotations = typing.get_type_hints(self.callable_object)
        if verify_types and annotations:
            test_type_hints = {}
            typed_example_values = {}
            for parameter_name, parameter_value in bound.arguments.items():
                type_hint = annotations.get(parameter_name, None)
                test_type_hints[parameter_name] = type_hint
                typed_example_values[parameter_name] = parameter_value

            if self.returns is not NotDefined and "return" in annotations:
                test_type_hints["return"] = annotations["return"]
                typed_example_values["returns"] = self.returns

            create_model(getattr(self.callable_object, __name__, "ExamplesModel"), **test_type_hints)(**typed_example_values)


class ExampleRegistry:


    def __init__(self):
        self.examples = []

    def add_call(self, *args, **kwargs):
        def add_example_wrapper(function):
            self.examples.append(Example(function, args=args, kwargs=kwargs))
            return function
        return add_example_wrapper

    def add_call_with_returns(self, _returns, *args, **kwargs):
        def add_example_wrapper(function):
            self.examples.append(Example(function, returns=_returns, args=args, kwargs=kwargs))
            return function
        return add_example_wrapper

    def verify_signatures(self, verify_types=True):
        for example in self.examples:
            example.verify_signature(verify_types=verify_types)
