from functools import singledispatch
from types import ModuleType
from typing import Any, Callable, List

from examples import registry
from examples.example import CallableExample


def example(*args, **kwargs) -> Callable:
    """A decorator that adds an example to the decorated function."""

    def wrap_example(function: Callable) -> Callable:
        attached_module_name = function.__module__
        if attached_module_name not in registry.module_registry:
            registry.module_registry[attached_module_name] = registry.Examples()
        module_registry = registry.module_registry[attached_module_name]
        return module_registry.example(*args, **kwargs)(function)

    return wrap_example


def example_returns(_returns: Any, *args, **kwargs) -> Callable:
    """A decorator that adds an example to the decorated function, with the first argument
       being an expected return value.
    """

    def wrap_example(function: Callable) -> Callable:
        attached_module_name = function.__module__
        if attached_module_name not in registry.module_registry:
            registry.module_registry[attached_module_name] = registry.Examples()
        module_registry = registry.module_registry[attached_module_name]
        return module_registry.example_returns(_returns, *args, **kwargs)(function)

    return wrap_example


@singledispatch
def get_examples(item: Any) -> List[CallableExample]:
    """Returns all examples associated with the provided item.
       Provided item should be of type function, module, or module name.
    """
    raise NotImplementedError(f"Currently examples can not be attached to {type(item)}.")


@get_examples.register
def _get_examples_callable(item: Callable) -> List[CallableExample]:
    """Returns all examples registered for a function"""
    module_examples = registry.module_registry.get(item.__module__, None)
    if not module_examples:
        return []

    return module_examples.get(item)


@get_examples.register
def _get_examples_module(item: ModuleType) -> List[CallableExample]:
    """Returns all examples registered to a module"""
    module_examples = registry.module_registry.get(item.__name__, None)
    return module_examples.examples if module_examples else []


@get_examples.register
def _get_examples_module_name(item: str) -> List[CallableExample]:
    """Returns all examples registered to a module name"""
    module_examples = registry.module_registry.get(item, None)
    return module_examples.examples if module_examples else []
