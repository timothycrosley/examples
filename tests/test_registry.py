from examples.registry import Examples


def test_doc_strings():
    my_examples = Examples()

    @my_examples.example(1, 2)
    def add(number_1: int, number_2: int) -> int:
        return number_1 + number_2

    assert add.__doc__ and "Examples" in add.__doc__ and "add" in add.__doc__ and "1" in add.__doc__

    my_docless_examples = Examples(add_to_doc_strings=False)

    @my_docless_examples.example(1, 2)
    def add_docless(number_1: int, number_2: int) -> int:
        return number_1 + number_2

    assert not add_docless.__doc__
