import inspect
from typing import Any, Callable, get_type_hints

from pydantic import create_model


class NotDefined:
    pass


class CallableExample:
    """Defines a single Example call against a callable."""

    def __init__(self, callable_object: Callable, args, kwargs, returns=NotDefined):
        self.args = args
        self.kwargs = kwargs
        self.callable_object = callable_object
        self.returns = returns

    def verify_signature(self, verify_types: bool = True):
        """Verifies that the example makes sense against the functions signature."""
        bound = inspect.signature(self.callable_object).bind(*self.args, **self.kwargs)

        annotations = get_type_hints(self.callable_object)
        if verify_types and annotations:
            test_type_hints = {}
            typed_example_values = {}
            for parameter_name, parameter_value in bound.arguments.items():
                type_hint = annotations.get(parameter_name, None)
                test_type_hints[parameter_name] = (type_hint, None)
                typed_example_values[parameter_name] = parameter_value

            if self.returns is not NotDefined and "return" in annotations:
                test_type_hints["return"] = annotations["return"]
                typed_example_values["returns"] = self.returns

            create_model(  # type: ignore
                getattr(self.callable_object, "__name__", "ExamplesModel"), **test_type_hints
            )(**typed_example_values)

    def use(self) -> Any:
        """Runs the given example, giving back the result returned from running the example call."""
        return self.callable_object(*self.args, **self.kwargs)

    def test(self, verify_return_type: bool = True):
        """Tests the given example, ensuring the return value matches that specified."""
        result = self.use()
        if self.returns is not NotDefined:
            if result != self.returns:
                raise AssertionError(
                    f"Example's expected return value of '{self.returns}' "
                    f"does not not match actual return value of `{result}`"
                )

        if verify_return_type:
            type_hints = get_type_hints(self.callable_object)
            if type_hints and "returns" in type_hints:
                create_model(  # type: ignore
                    getattr(self.callable_object, "__name__", "ExamplesModel"),
                    {"returns": type_hints["returns"]},
                )(returns=result)

    def verify_and_test(self, verify_types: bool = True) -> None:
        self.verify_signature(verify_types=verify_types)
        self.test(verify_return_type=verify_types)