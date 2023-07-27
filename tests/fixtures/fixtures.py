import pytest

from physities.src.entities.dimension import Dimension
from physities.src.entities.scale.basescale import BaseScale
from physities.src.enums.base_units import BaseUnit


def _dimensions_group_test():
    tuples = [(1, 0, 0, 0, 0), (0, 89, 0, 1, 4), (-1, -8.8, 0, 4.3333, 1)]
    dimensions = [Dimension.new_instance(dimensions_tuple=i) for i in tuples]
    return dimensions


@pytest.fixture()
def dimensions_group_test():
    return _dimensions_group_test()


def _conversion_tuple_test():
    return tuple({"from_base": 1, "to_base": 1} for i in BaseUnit)


@pytest.fixture()
def conversion_tuple_test():
    return _conversion_tuple_test()


@pytest.fixture()
def base_scales():
    xxx = []
    for dimension in _dimensions_group_test():
        conversion_tuple = _conversion_tuple_test()
        value = 19
        resize = 1
        result_attrs = {
            "dimension": dimension,
            "conversion_tuple": conversion_tuple,
            "resize": resize,
            "value": None,
        }
        xxx.append(BaseScale(BaseScale.__name__, (BaseScale,), result_attrs))
    return xxx
