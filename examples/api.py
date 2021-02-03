from functools import singledispatch
from types import FunctionType, ModuleType
from typing import Any, Callable, List

from examples import registry
from examples.example_objects import CallableExample, NotDefined


def example(
    *args,
    _example_returns: Any = NotDefined,
    _example_raises: Any = None,
    _example_doc_string: bool = True,
    **kwargs,
) -> Callable:
    """A decorator that adds an example to the decorated function.

    Everything passed in to the example will be passed into the wrapped function in the
    unchanged when testing or using the example.

    Except, for the following magic parameters (all prefixed with `_example_`):

    - *_example_returns*: The exact result you expect the example to return.
    - *_example_raises*: An exception you expect the example to raise (can't be combined with above)
    - *_example_doc_string*: If True example is added to the functions doc string.
    """

    def wrap_example(function: Callable) -> Callable:
        attached_module_name = function.__module__
        if attached_module_name not in registry.module_registry:
            registry.module_registry[attached_module_name] = registry.Examples()
        module_registry = registry.module_registry[attached_module_name]
        return module_registry.example(
            *args, _example_returns=_example_returns, _example_raises=_example_raises, **kwargs
        )(function)

    return wrap_example


def add_example_to(function: Callable) -> Callable:
    """Returns a function that when called will add an example to the provide function.

    This can be re-used multiple times to add multiple examples:

            add_example = add_example_to(my_sum_function)
            add_example(1, 2)
            add_example(2, 3, _example_returns=5)

    Or, can be used once for a single example:

            add_example_to(my_sum_function)(1, 1, _example_returns=5)

    The returned function follows the same signature as the @example decorator except
    it returns the produced examples, allowing you to expose it:

            add_example = add_example_to(my_sum_function)(1, 1)
    """

    def example_factory(
        *args,
        _example_returns: Any = NotDefined,
        _example_raises: Any = None,
        _example_doc_string: bool = True,
        **kwargs,
    ) -> CallableExample:
        example(
            *args,
            _example_returns=_example_returns,
            _example_raises=_example_raises,
            _example_doc_string=_example_doc_string,
            **kwargs,
        )(function)
        return get_examples(function)[-1]

    return example_factory


@singledispatch
def get_examples(item: Any) -> List[CallableExample]:
    """Returns all examples associated with the provided item.
       Provided item should be of type function, module, or module name.
    """
    raise NotImplementedError(f"Currently examples can not be attached to {type(item)}.")


@get_examples.register(FunctionType)
def _get_examples_callable(item: FunctionType) -> List[CallableExample]:
    """Returns all examples registered for a function"""
    module_examples = registry.module_registry.get(item.__module__, None)
    if not module_examples:
        return []

    return module_examples.get(item)


@get_examples.register(str)
def _get_examples_module_name(item: str) -> List[CallableExample]:
    """Returns all examples registered to a module name"""
    module_examples = registry.module_registry.get(item, None)
    return module_examples.examples if module_examples else []


@get_examples.register(ModuleType)
def _get_examples_module(item: ModuleType) -> List[CallableExample]:
    """Returns all examples registered to a module"""
    return _get_examples_module_name(item.__name__)


@singledispatch
def verify_signatures(item: Any, verify_types: bool = True) -> None:
    """Verifies the signature of all examples associated with the provided item.
       Provided item should be of type function, module, or module name.

       - *verify_types*: If `True` all examples will have have their types checked against
         their associated functions type annotations.
    """
    raise NotImplementedError(f"Currently examples can not be attached to {type(item)}.")


@verify_signatures.register(str)
def _verify_module_name_signatures(item: str, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module name."""
    module_examples = registry.module_registry.get(item, None)
    if not module_examples:
        raise ValueError(
            f"Tried verifying example signatures for {item} module but "
            "no examples are defined for that module."
        )
    module_examples.verify_signatures(verify_types=verify_types)


@verify_signatures.register(ModuleType)
def _verify_module_signatures(item: ModuleType, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module."""
    _verify_module_name_signatures(item.__name__, verify_types=verify_types)


@verify_signatures.register(FunctionType)
def _verify_function_signature(item: FunctionType, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module."""
    examples = get_examples(item)
    if not examples:
        raise ValueError(
            f"Tried verifying example signatures for {item} function but "
            "no examples are defined for that function."
        )

    for function_example in examples:
        function_example.verify_signature(verify_types=verify_types)


@singledispatch
def test_examples(item: Any, verify_return_type: bool = True) -> None:
    """Run all examples verifying they work as defined against the associated function.
       Provided item should be of type function, module, or module name.

       - *verify_return_type*: If `True` all examples will have have their return value types
         checked against their associated functions type annotations.
    """
    raise NotImplementedError(f"Currently examples can not be attached to {type(item)}.")


@test_examples.register(str)
def _test_module_name_examples(item: str, verify_return_type: bool = True) -> None:
    """Tests all examples associated with the provided module name."""
    module_examples = registry.module_registry.get(item, None)
    if not module_examples:
        raise ValueError(
            f"Tried testing example for {item} module but "
            "no examples are defined for that module."
        )
    module_examples.test_examples(verify_return_type=verify_return_type)


@test_examples.register(ModuleType)
def _test_module_examples(item: ModuleType, verify_return_type: bool = True) -> None:
    """Tests all examples associated with the provided module."""
    _test_module_name_examples(item.__name__, verify_return_type=verify_return_type)


@test_examples.register(FunctionType)
def _test_function_examples(item: FunctionType, verify_return_type: bool = True) -> None:
    """Tests all examples associated with the provided function."""
    examples = get_examples(item)
    if not examples:
        raise ValueError(
            f"Tried testing example for {item} function but "
            "no examples are defined for that function."
        )

    for function_example in examples:
        function_example.test(verify_return_type=verify_return_type)


@singledispatch
def verify_and_test_examples(item: Any, verify_return_type: bool = True) -> None:
    """Verifies the signature of all examples associated with the provided item then
       runs all examples verifying they work as defined.
       Provided item should be of type function, module, or module name.

       - *verify_types*: If `True` all examples will have have their types checked against
         their associated functions type annotations.
    """
    raise NotImplementedError(f"Currently examples can not be attached to {type(item)}.")


@verify_and_test_examples.register(str)
def _verify_and_test_module_name_examples(item: str, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module name."""
    module_examples = registry.module_registry.get(item, None)
    if not module_examples:
        raise ValueError(
            f"Tried verifying example signatures and running tests for {item} module "
            "but no examples are defined for that module."
        )
    module_examples.verify_and_test_examples(verify_types=verify_types)


@verify_and_test_examples.register(ModuleType)
def _verify_and_test_module_examples(item: ModuleType, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module."""
    _verify_and_test_module_name_examples(item.__name__, verify_types=verify_types)


@verify_and_test_examples.register(FunctionType)
def _verify_and_test_function_examples(item: FunctionType, verify_types: bool = True) -> None:
    """Verify signatures associated with the provided module."""
    examples = get_examples(item)
    if not examples:
        raise ValueError(
            f"Tried verifying example signatures and running tests for {item} function"
            " but no examples are defined for that function."
        )

    for function_example in examples:
        function_example.verify_and_test(verify_types=verify_types)


def verify_all_signatures(verify_types: bool = False) -> None:
    """Verify all examples against their associated functions signatures."""
    for module_name in registry.module_registry:
        verify_signatures(module_name, verify_types=verify_types)


def test_all_examples(verify_return_type: bool = False) -> None:
    """Tests all examples against their associated functions."""
    for module_name in registry.module_registry:
        test_examples(module_name, verify_return_type=verify_return_type)


def verify_and_test_all_examples(verify_types: bool = False) -> None:
    """Tests all examples while verifying them against their associated functions signatures."""
    for module_name in registry.module_registry:
        verify_and_test_examples(module_name, verify_types=verify_types)
