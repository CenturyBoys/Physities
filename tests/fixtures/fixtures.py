import pytest

from physities.src.dimension import Dimension
from physities.src.dimension.base_dimensions import BaseDimension


@pytest.fixture()
def dimension_sample():
    return Dimension.new_instance(dimensions_tuple=(-1, -8.8, 0, 4.3333, 1., 9.7, 9))


@pytest.fixture()
def from_base_conversion_sample():
    return -1, 0, 1, 2., 3, 4, 5
