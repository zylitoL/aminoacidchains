import numpy as np

from itertools import product
from typing import Iterator, Iterable

"""fastgenseq.py

A rewrite of genseq.py with local space in mind, and lower level data.

Functions to generate 2-dimensional non-isomorphic amino acid chains up to some
length. Our approach is to generate sequences of relative directions from an
origin (sequence of up,down,left,right, etc) through the ismorphism to
{0, 1, 2, 3}; in particular:
    0 -- up
    1 -- right
    2 -- down
    3 -- left
"""

def gendirs(length: int) -> Iterator[Iterable[int]]:
    """Generate all sequences of directions of length.

    A note on alternative approaches:
        This iteration is equivalent to iterating over all base-4 strings
        of specified length. As integers, this can be iterated by iterating
        to range(4 ** length). To obtain the base-4 representation, using a
        numpy approach is probably best -- numpy.base_repr. However, this is
        60x slower.
    Args:
        length (int): Length of sequence

    Yields:
        Iterator[Iterable[int]]: Iterator of direction sequences
    """
    yield product(range(4), repeat=length)