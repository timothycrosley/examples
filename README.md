[![eXamples - Python Tests and Documentation Done by Example.](https://raw.github.com/timothycrosley/examples/master/art/logo_large.png)](https://timothycrosley.github.io/examples/)
_________________

[![PyPI version](https://badge.fury.io/py/examples.svg)](http://badge.fury.io/py/examples)
[![Test Status](https://github.com/timothycrosley/examples/workflows/Test/badge.svg?branch=master)](https://github.com/timothycrosley/examples/actions?query=workflow%3ATest)
[![Lint Status](https://github.com/timothycrosley/examples/workflows/Lint/badge.svg?branch=master)](https://github.com/timothycrosley/examples/actions?query=workflow%3ALint)
[![codecov](https://codecov.io/gh/timothycrosley/examples/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/examples)
[![Join the chat at https://gitter.im/timothycrosley/examples](https://badges.gitter.im/timothycrosley/examples.svg)](https://gitter.im/timothycrosley/examples?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/examples/)
[![Downloads](https://pepy.tech/badge/examples)](https://pepy.tech/project/examples)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
_________________

[Read Latest Documentation](https://timothycrosley.github.io/examples/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/examples/)
_________________

**eXamples** (AKA: xamples for SEO) is a Python3 library enabling interactable, self-documenting, and self-verifying examples. These examples are attached directly to Python functions using decorators or via separate `MODULE_examples.py` source files.

[![Example Usage Gif](https://raw.githubusercontent.com/timothycrosley/examples/master/art/example.gif)](https://raw.githubusercontent.com/timothycrosley/examples/master/art/example.gif)

Key Features:

* **Simple and Obvious API**: Add `@examples.example(*args, **kwargs)` decorators for each example you want to add to a function.
* **Auto Documenting**: Examples, by default, get added to your functions docstring viewable both in interactive interpreters and when using [portray](https://timothycrosley.github.io/portray/) or [pdocs](https://timothycrosley.github.io/pdocs/).
* **Signature Validating**: All examples can easily be checked to ensure they match the function signature (and type annotations!) with a single call (`examples.verify_all_signatures()`).
* **Act as Tests**: Examples act as additional test cases, that can easily be verified using a single test case in your favorite test runner: (`examples.test_all_examples()`).
* **Async Compatibility**: Examples can be attached and tested as easily against async functions as non-async ones.

What's Missing:

* **Class Support**: Currently examples can only be attached to individual functions. Class and method support is planned for a future release.

## Quick Start

The following guides should get you up and running using eXamples in no time.

1. [Installation](https://timothycrosley.github.io/examples/docs/quick_start/1.-installation/) - TL;DR: Run `pip3 install examples` within your projects virtual environment.
2. [Adding Examples](https://timothycrosley.github.io/examples/docs/quick_start/2.-adding-examples/) -
    TL;DR: Add example decorators that represent each of your examples:

        # my_module_with_examples.py
        from examples import example

        @example(1, number_2=1, _example_returns=2)
        def add(number_1: int, number_2: int) -> int:
            return number_1 + number_2

3. [Verify and Test Examples](https://timothycrosley.github.io/examples/docs/quick_start/3.-testing-examples/) -
    TL;DR: run `examples.verify_and_test_examples` within your projects test cases.

        # test_my_module_with_examples.py
        from examples import verify_and_test_examples

        import my_module_with_examples


        def test_examples_verifying_signature():
            verify_and_test_examples(my_module_with_examples)

4. Introspect Examples -

        import examples

        from my_module_with_examples import add


        examples.get_examples(add)[0].use() == 2

## Why Create Examples?

I've always wanted a way to attach examples to functions in a way that would be re-useable for documentation, testing, and API proposes.
Just like moving Python parameter types from comments into type annotations has made them more broadly useful, I hope examples can do the same for example calls.

I hope you too find `eXamples` useful!

~Timothy Crosley
