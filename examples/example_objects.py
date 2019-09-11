import asyncio
import inspect
from pprint import pformat
from typing import Any, Callable, get_type_hints

from pydantic import create_model


class NotDefined:
    """This exists to allow distinctly checking for a parameter not passed in
       vs. one that is passed in as None.
    """

    pass


class CallableExample:
    """Defines a single Example call against a callable."""

    __slots__ = ("args", "kwargs", "callable_object", "returns", "raises")

    def __init__(
        self, callable_object: Callable, args, kwargs, returns: Any = NotDefined, raises: Any = None
    ):
        self.args = args
        self.kwargs = kwargs
        self.callable_object = callable_object
        if raises and returns is not NotDefined:
            raise ValueError("Cannot specify both raises and returns on a single example.")
        self.returns = returns
        self.raises = raises

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
        if inspect.iscoroutinefunction(self.callable_object):
            loop = asyncio.get_event_loop()
            call = self.callable_object(*self.args, **self.kwargs)
            if loop.is_running():
                return call  # pragma: no cover

            function = asyncio.ensure_future(call, loop=loop)
            loop.run_until_complete(function)
            return function.result()
        return self.callable_object(*self.args, **self.kwargs)

    def test(self, verify_return_type: bool = True):
        """Tests the given example, ensuring the return value matches that specified."""
        try:
            result = self.use()
        except BaseException as exception:
            if not self.raises:
                raise

            if (type(self.raises) == type and not isinstance(exception, self.raises)) or (
                type(self.raises) != type
                and (
                    not isinstance(exception, type(self.raises))
                    or self.raises.args != exception.args
                )
            ):
                raise AssertionError(
                    f"Example expected {repr(self.raises)} to be raised but "
                    f"instead {repr(exception)} was raised"
                )
            return

        if self.raises:
            raise AssertionError(
                f"Example expected {repr(self.raises)} to be raised "
                f"but instead {repr(result)} was returned"
            )
        elif self.returns is not NotDefined:
            if result != self.returns:
                raise AssertionError(
                    f"Example's expected return value of '{self.returns}' "
                    f"does not not match actual return value of `{result}`"
                )

        if verify_return_type:
            type_hints = get_type_hints(self.callable_object)
            if type_hints and "return" in type_hints:
                create_model(  # type: ignore
                    getattr(self.callable_object, "__name__", "ExamplesModel"),
                    returns=type_hints["return"],
                )(returns=result)

    def verify_and_test(self, verify_types: bool = True) -> None:
        self.verify_signature(verify_types=verify_types)
        self.test(verify_return_type=verify_types)

    def __str__(self):
        arg_str = ",\n    ".join(repr(arg) for arg in self.args)
        if self.kwargs:
            arg_str += ",\n    " if arg_str else ""
            arg_str += ",\n    ".join(
                f"{name}={repr(value)}" for name, value in self.kwargs.items()
            )

        call_str = f"{self.callable_object.__name__}(\n    {arg_str}\n)"
        if self.returns is not NotDefined:
            call_str += f"\n == \n{pformat(self.returns)}"
        elif self.raises:
            call_str += f"\nraises {pformat(self.raises)}"
        return call_str

    def __repr__(self):
        return f"Example:\n{str(self)}"
