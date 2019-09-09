import pytest

from examples import api
from examples.example_objects import CallableExample

from . import example_module_fail, example_module_pass, no_examples_module


def test_get_examples():
    with pytest.raises(NotImplementedError):
        api.get_examples(42)  # examples can't be associated to arbitrary types

    module_examples = api.get_examples(example_module_pass)
    assert module_examples == api.get_examples(example_module_pass.__name__)
    assert module_examples
    assert type(module_examples) == list
    for example in module_examples:
        assert type(example) == CallableExample

    function_examples = api.get_examples(example_module_pass.add)
    assert function_examples
    assert type(function_examples) == list
    for example in function_examples:
        assert type(example) == CallableExample

    assert api.get_examples(no_examples_module) == []
    assert api.get_examples(no_examples_module.function) == []


def test_verify_signatures():
    with pytest.raises(NotImplementedError):
        api.verify_signatures(42)  # examples can't be associated to arbitrary types

    with pytest.raises(ValueError):
        api.verify_signatures(no_examples_module.function)  # Examples must be defined

    with pytest.raises(ValueError):
        api.verify_signatures(no_examples_module)  # Examples must be defined

    api.verify_signatures(example_module_pass)
    api.verify_signatures(example_module_pass, verify_types=False)
    api.verify_signatures(example_module_pass.__name__)
    api.verify_signatures(example_module_pass.__name__, verify_types=False)
    api.verify_signatures(example_module_pass.add)
    api.verify_signatures(example_module_pass.add, verify_types=False)

    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail)
    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail, verify_types=False)
    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail.__name__)
    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail.__name__, verify_types=False)
    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail.add)
    with pytest.raises(Exception):
        api.verify_signatures(example_module_fail.add, verify_types=False)


def test_test_examples():
    with pytest.raises(NotImplementedError):
        api.test_examples(42)  # examples can't be associated to arbitrary types

    with pytest.raises(ValueError):
        api.test_examples(no_examples_module.function)  # Examples must be defined

    with pytest.raises(ValueError):
        api.test_examples(no_examples_module)  # Examples must be defined

    api.test_examples(example_module_pass)
    api.test_examples(example_module_pass, verify_return_type=False)
    api.test_examples(example_module_pass.__name__)
    api.test_examples(example_module_pass.__name__, verify_return_type=False)
    api.test_examples(example_module_pass.add)
    api.test_examples(example_module_pass.add, verify_return_type=False)

    with pytest.raises(Exception):
        api.test_examples(example_module_fail)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail, verify_return_type=False)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail.__name__)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail.__name__, verify_return_type=False)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail.add)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail.add, verify_return_type=False)
    with pytest.raises(Exception):
        api.test_examples(example_module_fail.multiply)


def test_verify_and_test_examples():
    with pytest.raises(NotImplementedError):
        api.verify_and_test_examples(42)  # examples can't be associated to arbitrary types

    with pytest.raises(ValueError):
        api.verify_and_test_examples(no_examples_module.function)  # Examples must be defined

    with pytest.raises(ValueError):
        api.verify_and_test_examples(no_examples_module)  # Examples must be defined

    api.verify_and_test_examples(example_module_pass)
    api.verify_and_test_examples(example_module_pass, verify_types=False)
    api.verify_and_test_examples(example_module_pass.__name__)
    api.verify_and_test_examples(example_module_pass.__name__, verify_types=False)
    api.verify_and_test_examples(example_module_pass.add)
    api.verify_and_test_examples(example_module_pass.add, verify_types=False)

    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail)
    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail, verify_types=False)
    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail.__name__)
    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail.__name__, verify_types=False)
    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail.add)
    with pytest.raises(Exception):
        api.verify_and_test_examples(example_module_fail.add, verify_types=False)


def test_verify_all_signatures():
    with pytest.raises(Exception):
        api.verify_all_signatures()
    with pytest.raises(Exception):
        api.verify_all_signatures(verify_types=False)


def test_test_all_examples():
    with pytest.raises(Exception):
        api.test_all_examples()
    with pytest.raises(Exception):
        api.test_all_examples(verify_return_type=False)


def test_verify_and_test_all_examples():
    with pytest.raises(Exception):
        api.verify_and_test_all_examples()
    with pytest.raises(Exception):
        api.verify_and_test_all_examples(verify_types=False)
