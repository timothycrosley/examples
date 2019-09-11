from examples.api import (
    add_example_to,
    example,
    get_examples,
    test_all_examples,
    test_examples,
    verify_all_signatures,
    verify_and_test_all_examples,
    verify_and_test_examples,
    verify_signatures,
)
from examples.registry import Examples

__version__ = "0.1.1"
__all__ = [
    "__version__",
    "add_example_to",
    "example",
    "example_returns",
    "get_examples",
    "verify_signatures",
    "test_examples",
    "verify_and_test_examples",
    "verify_all_signatures",
    "test_all_examples",
    "verify_and_test_all_examples",
    "Examples",
]
