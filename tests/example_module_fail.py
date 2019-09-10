from examples import example


@example(1, 2)
@example(number_1=1, number_2=1, _example_returns=2)
@example()
def add(number_1: int, number_2: int = 1) -> int:
    return number_1 + number_2


@example(3, 2, _example_returns="apple")
@example(2, 2)
def multiply(number_1: int, number_2: int) -> int:
    return number_1 * number_2
