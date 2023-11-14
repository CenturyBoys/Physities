import pytest

from physities.src.dimension import Dimension
from physities.src.scale.basescale import BaseScale
from physities.src.dimension.base_dimensions import BaseDimension


def _dimensions_group_test():
    tuples = [(1, 0, 0, 0, 0, 0, 0), (0, 89, 0, 1, 4, 6, 0), (-1, -8.8, 0, 4.3333, 1., 9.7, 9)]
    dimensions = [Dimension.new_instance(dimensions_tuple=i) for i in tuples]
    return dimensions


@pytest.fixture()
def dimensions_group_test():
    return _dimensions_group_test()


def _conversion_tuple_test():
    return tuple(1 for i in BaseDimension)


@pytest.fixture()
def conversion_tuple_test():
    return _conversion_tuple_test()


