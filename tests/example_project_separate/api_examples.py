"""This is the example portion of an example that demonstrates examples and implementation separate.

One potential example about this pattern is the examples add **no** overhead unless imported.
"""
from examples import add_example_to

from .api import add, multiply

add_example = add_example_to(add)
add_example(1, 1)
add_example(2, 2, _example_returns=4)

multiply_example = add_example_to(multiply)
multiply_example(2, 2)
multiply_example(1, 1, _example_returns=1)
