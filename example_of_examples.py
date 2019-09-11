from examples import example


@example(1, 1, _example_returns=2)
def add(number_1: int, number_2: int) -> int:
    return number_1 + number_2


@example(2, 2, _example_returns=4)
@example(1, 1)
def multiply(number_1: int, number_2: int) -> int:
    """Multiply two numbers_together"""
    return number_1 * number_2
