from typing import Any, Callable, Dict, List, Optional

from examples.example_objects import CallableExample, NotDefined


class Examples:
    """An object that holds a set of examples as they are registered."""

    __slots__ = ("examples", "add_to_doc_strings", "_callable_mapping")

    def __init__(self, add_to_doc_strings: bool = True):
        self.examples: List[CallableExample] = []
        self.add_to_doc_strings: bool = add_to_doc_strings
        self._callable_mapping: Dict[Callable, list] = {}

    def _add_to_doc_string(self, function: Callable, example: CallableExample) -> None:
        if function.__doc__ is None:
            function.__doc__ = ""

        indent: int = 4
        for line in reversed(function.__doc__.split("\n")):
            if line.strip():
                indent = len(line) - len(line.lstrip(" "))
        indent_spaces: str = " " * indent

        if "Examples:" not in function.__doc__:
            function.__doc__ += f"\n\n{indent_spaces}Examples:\n\n"

        indented_example = str(example).replace("\n", f"\n{indent_spaces}        ")
        function.__doc__ += f"{indent_spaces}-\n{indent_spaces}        {indented_example}"

    def example(
        self,
        *args,
        _example_returns: Any = NotDefined,
        _example_raises: Any = None,
        _example_doc_string: Optional[bool] = None,
        **kwargs,
    ) -> Callable:
        def example_wrapper(function):
            new_example = CallableExample(
                function, returns=_example_returns, raises=_example_raises, args=args, kwargs=kwargs
            )
            self._callable_mapping.setdefault(function, []).append(new_example)
            if _example_doc_string or (_example_doc_string is None and self.add_to_doc_strings):
                self._add_to_doc_string(function, new_example)
            self.examples.append(new_example)
            return function

        return example_wrapper

    def verify_signatures(self, verify_types: bool = True) -> None:
        for example in self.examples:
            example.verify_signature(verify_types=verify_types)

    def test_examples(self, verify_return_type: bool = True) -> None:
        for example in self.examples:
            example.test(verify_return_type=verify_return_type)

    def verify_and_test_examples(self, verify_types: bool = True) -> None:
        for example in self.examples:
            example.verify_and_test(verify_types=verify_types)

    def get(self, function: Callable) -> List[CallableExample]:
        """Returns back any examples registered for a specific function"""
        return self._callable_mapping.get(function, [])


module_registry: Dict[str, Examples] = {}
