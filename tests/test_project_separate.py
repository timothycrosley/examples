import examples

from .example_project_separate import api, api_examples


def test_separate_project_examples():
    examples.verify_and_test_examples(api)
