from examples import example, example_returns


@example(1, 2)
@example(1)
@example_returns(2, number_1=1, number_2=1)
def add(number_1: int, number_2: int = 1) -> int:
    return number_1 + number_2


@example(2, 2)
@example_returns(6, 3, 2)
def multiply(number_1: int, number_2: int) -> int:
    return number_1 * number_2
